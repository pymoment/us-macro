import os
from glob import glob
import re
import json
import subprocess
import collections
from hashlib import sha1
from dateutil.parser import parse


def is_date(string):
    try:
        parse(string)
        return True
    except ValueError:
        return False


def get_output(cmd, show_command=False, prompt='$ '):
    try:
        output = subprocess.check_output(cmd,
                                         stderr=subprocess.DEVNULL,
                                         shell=True).decode()
    except subprocess.CalledProcessError as e:
        raise RuntimeError(e)
    if show_command:
        return '{}{}\n{}'.format(prompt, cmd, output)
    else:
        return output.strip()


def short_repr(obj, noneAsNA=False, n1=25, n2=12):
    '''Return a short representation of obj for clarity.'''
    if obj is None:
        return 'unspecified' if noneAsNA else 'None'
    elif isinstance(obj, str) and len(obj) > (n1+n2):
        return repr('{} ... {}').format(obj[:(n1-2)].replace('\n', '\\n'),
                                        obj[-n2:].replace('\n', '\\n').lstrip())
    elif isinstance(obj, (str, int, float, bool))\
            or (isinstance(obj, collections.Sequence)
                and len(obj) <= 2) or len(str(obj)) < (n1+n2):
        return repr(obj)
    elif isinstance(obj, collections.Sequence):  # should be a list or tuple
        return f'[{short_repr(obj[0])}, ...] ({len(obj)} items)'
    elif isinstance(obj, dict):
        if obj:
            first_key = list(obj.keys())[0]
            return f'{{{first_key!r}:{short_repr(obj[first_key])!r}, ...}} ({len(obj)} items)'
        else:
            return '{}'
    else:
        return f'{repr(obj)[:n1]} ...'


def compare_versions(v1, v2):
    # This will split both the versions by '.'
    arr1 = v1.split(".")
    arr2 = v2.split(".")
    # Initializer for the version arrays
    i = 0
    # We have taken into consideration that both the
    # versions will contains equal number of delimiters
    while(i < len(arr1)):
        # Version 2 is greater than version 1
        if int(arr2[i]) > int(arr1[i]):
            return -1
        # Version 1 is greater than version 2
        if int(arr1[i]) > int(arr2[i]):
            return 1
        # We can't conclude till now
        i += 1
    # Both the versions are equal
    return 0


def get_commit_link(repo, cid):
    bits = os.path.split(repo)
    if "github.com" or "gitlab.com" in bits:
        return "{}/commit/{}".format(repo, cid)
    elif "bitbucket.org" in bits:
        return "{}/commits/{}".format(repo, cid)
    else:
        return repo


def get_notebook_link(repo, cid, fn):
    bits = os.path.split(repo)
    if "github.com" or "gitlab.com" in bits:
        link = "{}/blob/{}/{}".format(repo, cid, fn)
        return '<a href=\\"{}\\"><code>{}</code></a>'.format(link, fn)
    else:
        return '<code>{}</code>'.format(fn)


def get_commit_info(fn, conf):
    out = ''
    if conf['add_commit_info']:
        try:
            long_fmt = get_output('git log -n 1 --pretty=format:%H -- {}'.format(fn))
            short_fmt = get_output('git log -n 1 --pretty=format:%h -- {}'.format(fn))
            rev_string = 'by {} on {} <a href=\\"{}\\">revision {}, {}</a>'.\
                format(get_output('git log -n 1 --format="%an" {}'.format(long_fmt)),
                       get_output('git show -s --format="%cd" --date=local {}'.format(long_fmt)),
                       get_commit_link(conf['repo'], long_fmt),
                       get_output('git log --oneline {} | wc -l'.format(fn)), short_fmt)
            out = '<p><small>Exported from {} committed {} {}</small></p>'.\
                  format(get_notebook_link(conf['repo'], long_fmt, fn), rev_string,
                         '<a href=\\"{}\\">{}</a>'.
                         format(conf['__about_commit__'],
                                '<span class=\\"fa fa-question-circle\\"></span>')
                         if conf['__about_commit__'] else '')
        except RuntimeError:
            # if git related command fails, indicating it is not a git repo
            # I'll just pass ...
            pass
    return out.replace('/', r'\/')


def get_nav(dirs, home_label, prefix='./'):
    if home_label:
        out = '''
<li class="nav-item">
  <a class="nav-link" href="{}index.html">{}</a>
</li>
        '''.format(prefix, home_label)
    else:
        out = ''
    for item in dirs:
        out += '''
<li class="nav-item">
  <a class="nav-link" href="{}{}{}">{}</a>
</li>
        '''.format(prefix, item,
                   '/index.html'
                   if os.path.isfile(f'{item}/{item}.ipynb') or os.path.isfile(f'{item}/{item}.Rmd')
                   else '.html',
                   ' '.join([x.capitalize() if x.upper() != x else x for x in item.split('_')]))
    return out


def get_right_nav(repo, source_label):
    if source_label:
        return '''
<ul class="navbar-nav">
<li class="nav-item">
   <a class="nav-link" href="%s"> %s </a>
</li>
</ul>
        ''' % (repo, source_label)
    else:
        return ''


def get_font(font):
    if font is None:
        return ''
    else:
        return 'font-family: "{}";'.format(font)


def get_sidebar(path):
    return '''
<script>
$( document ).ready(function(){
    // depth of toc (number of levels)
    var cfg={'threshold':{{ nb.get('metadata', {}).get('toc', {}).get('threshold', '3') }},
     'number_sections': false,
     'toc_cell': false,          // useless here
     'toc_window_display': true, // display the toc window
     "toc_section_display": "block", // display toc contents in the window
     'sideBar':true,       // sidebar or floating window
     'navigate_menu':false       // navigation menu (only in liveNotebook -- do not change)
    }
    var st={};                  // some variables used in the script
    st.rendering_toc_cell = false;
    st.config_loaded = false;
    st.extension_initialized=false;
    st.nbcontainer_marginleft = $('#notebook-container').css('margin-left')
    st.nbcontainer_marginright = $('#notebook-container').css('margin-right')
    st.nbcontainer_width = $('#notebook-container').css('width')
    st.oldTocHeight = undefined
    st.cell_toc = undefined;
    st.toc_index=0;
    // fire the main function with these parameters
    table_of_contents(cfg, st);
    var file=%sDict[$("h1:first").attr("id")];
    $("#toc-level0 a").css("color","#126dce");
    $('a[href="#'+$("h1:first").attr("id")+'"]').hide()
    var docs=%sArray;
    var docs_map=%sArrayMap;
    var pos=%sArray.indexOf(file);
    for (var a=pos;a>=0;a--){
      $('<li><a href="'+docs[a]+'.html"><font color="#073642"><b>' +
        docs_map[docs[a]].replace(/_/g," ") +
        '</b></font></a></li>').insertBefore("#toc-level0 li:eq(0)");
    }
    $('a[href="'+file+'.html'+'"]').css("color","#126dce");
    for (var a=pos+1;a<docs.length;a++){
      $(".toc #toc-level0").append('<li><a href="' +
      docs[a] +
      '.html"><font color="#073642"><b>' +
      docs_map[docs[a]].replace(/_/g," ") +
      '</b></font></a></li>');
    }
    // $("#toc-header").hide(); // comment out because it prevents search bar from displaying
    });
</script>
''' % (path, path, path, path)


def get_disqus(name):
    if name is None:
        return ''
    return '''
        <div id="disqus_thread"></div>
        <script type="text/javascript">
            /* * * CONFIGURATION VARIABLES: EDIT BEFORE PASTING INTO YOUR WEBPAGE * * */
            var disqus_shortname = '%s'; // required: replace example with your forum shortname

            /* * * DON'T EDIT BELOW THIS LINE * * */
            (function() {
                var dsq = document.createElement('script');
                dsq.type = 'text/javascript'; dsq.async = true;
                dsq.src = '//' + disqus_shortname + '.disqus.com/embed.js';
                (document.getElementsByTagName('head')[0] ||
                 document.getElementsByTagName('body')[0]).appendChild(dsq);
            })();
        </script>
        <noscript>
            Please enable JavaScript to view the &nbsp;
            <a href="http://disqus.com/?ref_noscript">comments powered by Disqus.</a>
        </noscript>
        <a href="http://disqus.com" class="dsq-brlink">
            comments powered by <span class="logo-disqus">Disqus</span>
        </a>
    ''' % name


def get_navbar(name, nav, right_nav, isRoot=False):
    return '''
<nav class="navbar navbar-expand-lg navbar-light bg-light">
    <a class="navbar-brand" href="{pre}index.html">{n}</a>
    <button type="button" class="navbar-toggler collapsed" data-toggle="collapse" data-target="#navbar" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div id="navbar" class="navbar-collapse collapse">
      <ul class="navbar-nav mr-auto">
        {nav}
      </ul>
        {r_nav}
    </div><!--/.nav-collapse -->
</nav><!--/.navbar -->
    '''.format(n=name, nav=nav, r_nav=right_nav, pre=('' if isRoot else '../'))


def get_index_tpl(conf, dirs):
    '''Generate index template at given paths'''
    content = '''
{%%- extends 'basic.tpl' -%%}

{%%- block header -%%}
{{ super() }}

<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta name="ipynb_website:version" content="%(version)s" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<meta name="twitter:card" content="summary"></meta>
<meta property="og:title" content="%(name)s" />
<meta property="og:type" content="article" />
<meta property="og:description" content="REPLACEMEDESCRIPTION" />

<title>%(name)s</title>

%(common_style)s
%(common_javascript)s

<style type="text/css">code{white-space: pre;}</style>

<script>hljs.initHighlightingOnLoad();</script>
<script type="text/javascript">
if (window.hljs && document.readyState && document.readyState === "complete") {
   window.setTimeout(function() {
      hljs.initHighlighting();
   }, 0);
}
</script>
<style type="text/css">
  div.input_prompt {display: none;}
  div.output_html {
     font-family: "PT Mono", monospace;
     font-size: 10.0pt;
     color: #353535;
     padding-bottom: 25px;
 }
  pre:not([class]) {
    background-color: white;
  }
</style>

%(mathjax_init)s

</head>

<body>
<style type = "text/css">
    @font-face {
     font-family: 'Droid Sans';
     font-weight: normal;
     font-style: normal;
     src: local('Droid Sans'), url('fonts/droid-sans.ttf') format('truetype');
    }
    @font-face {
     font-family: 'Fira Code';
     font-weight: normal;
     font-style: normal;
     src: local('Fira Code'), url('fonts/firacode.otf') format('opentype');
    }
    @font-face {
     font-family: 'PT Mono';
     font-weight: normal;
     font-style: normal;
     src: local('PT Mono'), url('fonts/ptmono.ttf') format('truetype');
    }

    body {
      %(font)s
    }

    h1, h2, h3, h4, h5, h6 {
      margin-top: 20px;
     }

    a.anchor-link:link {
      text-decoration: none;
      padding: 0px 20px;
      visibility: hidden;
    }

    h1:hover .anchor-link,
    h2:hover .anchor-link,
    h3:hover .anchor-link,
    h4:hover .anchor-link,
    h5:hover .anchor-link,
    h6:hover .anchor-link {
      visibility: hidden;
    }

    .main-container {
      max-width: 940px;
      margin-left: auto;
      margin-right: auto;
    }
    code {
      color: inherit;
      background-color: rgba(0, 0, 0, 0.04);
    }
    img {
      max-width:100%%;
      height: auto;
    }
    .tabbed-pane {
      padding-top: 12px;
    }
    button.code-folding-btn:focus {
      outline: none;
    }
</style>

%(active_page)s

<div class="container-fluid main-container">

<!-- tabsets -->
<script src="site_libs/navigation-1.1/tabsets.js"></script>
<script>
$(document).ready(function () {
  window.buildTabsets("TOC");
});
</script>

<!-- code folding -->

%(navbar)s

{%%- endblock header -%%}
{%% block footer %%}
<hr>
%(footer)s
<!-- To enable disqus, uncomment the section below and provide your disqus_shortname -->
%(disqus)s
</div>

%(pandoc_to_bs4)s

<!-- dynamically load mathjax for compatibility with self-contained -->
<script>
  (function () {
    var script = document.createElement("script");
    script.type = "text/javascript";
    script.src  = "https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.2/MathJax.js?config=TeX-MML-AM_CHTML";
    document.getElementsByTagName("head")[0].appendChild(script);
  })();
</script>

<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=UA-9902895-3"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'UA-9902895-3');
</script>

</body>
</html>
{%% endblock %%}
''' % {
        'version': conf['__version__'],
        'common_style': get_common_stylesheets(nested=False),
        'common_javascript': get_common_javascript(),
        'mathjax_init': get_mathjax_init(),
        'active_page': get_active_page(),
        'font': get_font(conf['font']),
        'name': conf['name'],
        'navbar': get_navbar(conf['name'],
                             get_nav([x for x in dirs if x not in conf['hide_navbar']],
                                     conf['homepage_label']),
                             get_right_nav(conf['repo'], conf['source_label'])),
        'pandoc_to_bs4': convert_pandoc_to_bs4(),
        'footer': conf['footer'],
        'disqus': get_disqus(conf['disqus'])
    }
    return content


def get_sos_tpl(option):
    if option == "header":
        return '''
{%- if nb['metadata'].get('sos',{}).get('kernels',none) is not none -%}

<style type="text/css">

table {
   padding: 0;
   border-collapse: collapse; }
thead {
    border-bottom-width: 1px;
    border-bottom-color: rgb(0,0,0);
    border-bottom-style: solid;
}
table tr {
   border: none;
   background-color: white;
   margin: 0;
   padding: 0; }
table tr:nth-child(2n) {
   background-color: #f8f8f8; }
table tr th {
   font-weight: bold;
   border: none;
   margin: 0;
   padding: 6px 13px; }
table tr td {
   border: none;
   margin: 0;
   padding: 6px 13px; }
table tr th :first-child, table tr td :first-child {
   margin-top: 0; }
table tr th :last-child, table tr td :last-child {
   margin-bottom: 0; }

.dataframe_container { max-height: 400px }
.dataframe_input {
    border: 1px solid #ddd;
    margin-bottom: 5px;
}

.rendered_html table {
  border: none;
}

.sos_hint {
  color: rgba(0,0,0,.4);
  font-family: monospace;
  display: none;
}

.output_stderr {
    display: none;
}
/*
 div.input {
     display: none;
 }
*/
.hidden_content {
    display: none;
}

.input_prompt {
    display: none;
}

.output_area .prompt {
    display: none;
}

.output_prompt {
    display: none;
}

#nextsteps {
   color: blue;
}

.scatterplot_by_rowname div.xAxis div.tickLabel {
    transform: translateY(15px) translateX(15px) rotate(45deg);
    -ms-transform: translateY(15px) translateX(15px) rotate(45deg);
    -moz-transform: translateY(15px) translateX(15px) rotate(45deg);
    -webkit-transform: translateY(15px) translateX(15px) rotate(45deg);
    -o-transform: translateY(15px) translateX(15px) rotate(45deg);
    /*rotation-point:50% 50%;*/
    /*rotation:270deg;*/
}

div.cell {
    padding: 0pt;
    border-width: 0pt;
}
.sos_dataframe td, .sos_dataframe th, .sos_dataframe tr {
    white-space: nowrap;
    border: none;
}

.sos_dataframe tr:hover {
    background-color: #e6f2ff;
}

.display_control_panel  {
    position: inherit;
    z-index: 1000;
}

.display_checkboxes {
    margin-top: 5pt;
}

{%- if nb['metadata'].get('sos',{}).get('kernels',none) is not none -%}

{% for item in nb['metadata'].get('sos',{}).get('kernels',{}) %}

{%- if item[2] -%}
.lan_{{item[0]}} .input_prompt { background-color: {{item[3]}} !important }

{%- else -%}
.lan_{{item[0]}} {}

{%- endif -%}

{% endfor %}

{%- endif -%}
</style>

<script>

function filterDataFrame(id) {
    var input = document.getElementById("search_" + id);
    var filter = input.value.toUpperCase();
    var table = document.getElementById("dataframe_" + id);
    var tr = table.getElementsByTagName("tr");

    // Loop through all table rows, and hide those who don't match the search query
    for (var i = 1; i < tr.length; i++) {
        for (var j = 0; j < tr[i].cells.length; ++j) {
            var matched = false;
            if (tr[i].cells[j].innerHTML.toUpperCase().indexOf(filter) != -1) {
                tr[i].style.display = "";
                matched = true
                break;
            }
            if (!matched)
                tr[i].style.display = "none";
        }
    }
}

function sortDataFrame(id, n, dtype) {
    var table = document.getElementById("dataframe_" + id);

    var tb = table.tBodies[0]; // use `<tbody>` to ignore `<thead>` and `<tfoot>` rows
    var tr = Array.prototype.slice.call(tb.rows, 0); // put rows into array

    if (dtype === 'numeric') {
        var fn = (a, b) =>
            parseFloat(a.cells[n].textContent) <= parseFloat(b.cells[n].textContent) ? -1 : 1;
    } else {
        var fn = (a, b) => {
            var c = a.cells[n].textContent.trim().localeCompare(b.cells[n].textContent.trim());
            return c > 0 ? 1 : (c < 0 ? -1 : 0) }
    }
    var isSorted = function(array, fn) {
        if (array.length < 2)
            return 1;
        var direction = fn(array[0], array[1]);
        for (var i = 1; i < array.length - 1; ++i) {
            var d = fn(array[i], array[i+1]);
            if (d == 0)
                continue;
            else if (direction == 0)
                direction = d;
            else if (direction != d)
                return 0;
            }
        return direction;
    }

    var sorted = isSorted(tr, fn);

    if (sorted == 1 || sorted == -1) {
        // if sorted already, reverse it
        for(var i = tr.length - 1; i >= 0; --i)
            tb.appendChild(tr[i]); // append each row in order
    } else {
        tr = tr.sort(fn);
        for(var i = 0; i < tr.length; ++i)
            tb.appendChild(tr[i]); // append each row in order
    }
}

function toggle_source() {
    var btn = document.getElementById("show_cells");
    if (btn.checked) {
        $('div.input').css('display', 'flex');
        $('.hidden_content').show();
        // this somehow does not work.
        $('div.cell').css('padding', '0pt').css('border-width', '0pt');
    } else {
        $('div.input').hide();
        $('.hidden_content').hide();
        $('div.cell').css('padding', '0pt').css('border-width', '0pt');
    }
}

function toggle_prompt() {
    var btn = document.getElementById("show_prompt");
    if (btn.checked) {
        $('.output_prompt').show();
        $('.input_prompt').show();
        $('.output_area .prompt').show();
    } else {
        $('.output_prompt').hide();
        $('.input_prompt').hide();
        $('.output_area .prompt').hide();
    }
}

function toggle_messages() {
    var btn = document.getElementById("show_messages");
    if (btn.checked) {
        $('.sos_hint').show();
        $('.output_stderr').show();
    } else {
        $('.output_stderr').hide();
        $('.sos_hint').hide();
    }
}

</script>

{%- endif -%}
    '''
    elif option == "panel":
        return '''
<div class='display_control_panel'>
    <div class="display_checkboxes">
    Show:
        &nbsp;
        <input type="checkbox" id="show_cells" name="show_cells" onclick="toggle_source()">
        <label for="show_cells">All cells</label>
        &nbsp;
        <input type="checkbox" id="show_prompt" name="show_prompt" onclick="toggle_prompt()">
        <label for="show_prompt">Prompt</label>
        &nbsp;
        <input type="checkbox" id="show_messages" name="show_messages" onclick="toggle_messages()">
        <label for="show_messages">Messages</label>
    </div>
</div>
    '''
    elif option == "body":
        return '''
{%- block input -%}

    {%- if 'scratch' in cell.metadata.tags -%}
        {%- elif 'report_cell' in cell.metadata.tags -%}
        {{ super() }}
    {%- else -%}
        <div class="hidden_content">
        {{ super() }}
        </div>
   {%- endif -%}
{%- endblock input -%}

{% block output %}
    {%- if 'report_output' in cell.metadata.tags -%}
        {{ super() }}
    {%- elif 'report_cell' in cell.metadata.tags -%}
        {{ super() }}
    {%- elif 'scratch' in cell.metadata.tags -%}
    {%- else -%}
        <div class="hidden_content">
        {{ super() }}
        </div>
   {%- endif -%}
{% endblock output %}

{% block markdowncell %}
    {%- if 'hide_output' in cell.metadata.tags -%}
        <div class="hidden_content">
        {{ super() }}
        </div>
    {%- elif 'scratch' in cell.metadata.tags -%}
    {%- else -%}
        {{ super() }}
   {%- endif -%}
{%- endblock markdowncell -%}


{% block codecell %}

{%- if cell['metadata'].get('kernel',none) is not none -%}
    <div class="rendered lan_{{cell['metadata'].get('kernel', none)}}">
    {{ super() }}
    </div>
{%- else -%}
    {{ super() }}
{%- endif -%}

{%- endblock codecell %}
        '''
    else:
        return ''


def get_common_javascript():
    return '''
<!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
<!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
<!--[if lt IE 9]>
  <script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>
  <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
<![endif]-->

<!-- Bootstrap 4 -->
<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>

<!-- Vega/Vegalite -->
<script src="https://cdn.jsdelivr.net/npm/vega@3"></script>
<script src="https://cdn.jsdelivr.net/npm/vega@5"></script>
<script src="https://cdn.jsdelivr.net/npm/vega-lite@2"></script>
<script src="https://cdn.jsdelivr.net/npm/vega-lite@3"></script>
<script src="https://cdn.jsdelivr.net/npm/vega-embed@3"></script>

<script src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@9.18.1/build/highlight.min.js"></script>

<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.2/MathJax.js?config=TeX-MML-AM_CHTML"></script>
    '''


def get_common_stylesheets(nested=True):
    return '''
<link rel="stylesheet"
    href="{0}css/jt.css">
<link rel="stylesheet"
    href="{0}css/toc2.css">
<link rel="stylesheet"
    href="{0}site_libs/jqueryui-1.11.4/jquery-ui.css">
<link rel="stylesheet"
    href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
<link rel="stylesheet"
    href="https://cdn.jsdelivr.net/npm/font-awesome@4.7.0/css/font-awesome.min.css">
<link rel="stylesheet"
    href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@9.18.1/build/styles/default.min.css">
    '''.format('' if not nested else '../')


def get_highlightjs_init():
    return '''
<script>hljs.initHighlightingOnLoad();</script>
<script type="text/javascript">
    if (window.hljs &&
        document.readyState &&
        document.readyState === "complete") {
       window.setTimeout(() => {
          hljs.initHighlighting();
       }, 0);
    }
</script>
    '''


def get_mathjax_init():
    return '''
<script>
    MathJax.Hub.Config({
        extensions: ["tex2jax.js"],
        jax: ["input/TeX", "output/HTML-CSS"],
        tex2jax: {
            inlineMath: [ ['$','$'], ["\\\\(","\\\\)"] ],
            displayMath: [ ['$$','$$'], ["\\\\[","\\\\]"] ],
            processEscapes: true
        },
        "HTML-CSS": {
            preferredFont: "TeX",
            availableFonts: ["TeX"],
            styles: {
                scale: 110,
                ".MathJax_Display": {
                    "font-size": "110%%",
                }
            }
        }
    });
</script>
    '''


def get_active_page():
    return '''
<script>
    // manage active state of menu based on current page
    $(document).ready(function () {
      // active menu anchor
      href = window.location.pathname
      href = href.substr(href.lastIndexOf('/') + 1)
      if (href === "")
        href = "index.html";
      var menuAnchor = $('a[href*="' + href + '"]');
      // mark it active
      menuAnchor.parent().addClass('active');
      // if it's got a parent navbar menu mark it active as well
      menuAnchor.closest('li.dropdown').addClass('active');
    });
</script>
    '''


def convert_pandoc_to_bs4():
    return '''
<script>
// TODO - some, or all of this could be moved to pre-rendering sed/regex
// add bootstrap table styles to pandoc tables (notebooks)
$(document).ready( () => {

  $('tr').parent('thead').parent('table').addClass('table table-condensed');
  $('tr').parent('thead').parent('table').removeAttr('border');
  $('tr').parent('thead').parent('table').removeClass('dataframe');

  $('.output_area .output_html table thead tr').removeAttr('style');
  $('.output_area .output_html table thead tr th').attr("scope", "col");

  $('.output_area .output_html table tbody tr th').attr("scope", "row");


  // Change the input cell gutter text, make it a link
  $('.input .input_prompt').map((n, e) => {
    e.innerHTML = `<a href="#" >Show Code Cell [${n + 1}]</a>`;
  });

  // Attach an event listener to the above link for show/hide
  $('.input .input_prompt a').map((n, e) => {
    const showOrHide = e => {
      e.preventDefault();
      $(`#code-${n}`).find('.inner_cell').toggleClass('collapse');
      const v = $(`#code-${n}`).find('.input_prompt a');
      if (v.html().includes('Show')) {
        v.html(`Hide Code Cell [${n+1}]`);
      } else {
        v.html(`Show Code Cell [${n+1}]`);
      }
    }

    e.addEventListener("click", showOrHide, false);
  });

  // Annotate parent cells of input cells with id/classes
  $('.input .inner_cell').map((n, e) => {
    $('.input .inner_cell').parent('div').toArray()[n].id = `code-${n}`;
  });
  $('.input .inner_cell')
    .addClass("collapse")
    .after('<div class="inner_cell" style="font-size: 150%; padding-left: 5px;">...</div>');

});
</script>
    '''


def get_notebook_tpl(conf, dirs, path):
    '''Generate notebook template at given path'''
    content = '''
{%%- extends 'basic.tpl' -%%}

{%%- block header -%%}
{{ super() }}
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta name="ipynb_website:version" content="%(version)s" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<meta name="twitter:card" content="summary_large_image"></meta>
<meta property="og:title" content="%(name)s | REPLACEMETITLE" />
<meta property="og:type" content="article" />
<meta property="og:description" content="REPLACEMEDESCRIPTION" />
<meta property="og:img" content="REPLACEMEIMAGE" />

<!-- begin stylesheets -->
%(common_style)s
%(user_style)s
<!-- end stylesheets -->

<!-- begin javascript -->
%(common_javascript)s
<!-- end javascript -->

%(highlightjs_init)s

<script src="../js/doc_toc.js"></script>
<script src="../js/docs.js"></script>

%(mathjax_init)s

<script>
function filterDataFrame(id) {
    var input = document.getElementById("search_" + id);
    var filter = input.value.toUpperCase();
    var table = document.getElementById("dataframe_" + id);
    var tr = table.getElementsByTagName("tr");
    // Loop through all table rows, and hide those who don't match the search query
    for (var i = 1; i < tr.length; i++) {
        for (var j = 0; j < tr[i].cells.length; ++j) {
            var matched = false;
            if (tr[i].cells[j].innerHTML.toUpperCase().indexOf(filter) != -1) {
                tr[i].style.display = "";
                matched = true
                break;
            }
            if (!matched)
                tr[i].style.display = "none";
        }
    }
}

function sortDataFrame(id, n, dtype) {
    var table = document.getElementById("dataframe_" + id);
    var tb = table.tBodies[0]; // use `<tbody>` to ignore `<thead>` and `<tfoot>` rows
    var tr = Array.prototype.slice.call(tb.rows, 0); // put rows into array
    if (dtype === 'numeric') {
        var fn = (a, b) =>
            parseFloat(a.cells[n].textContent) <= parseFloat(b.cells[n].textContent) ? -1 : 1;
    } else {
        var fn = function(a, b) {
            var c = a.cells[n].textContent.trim().localeCompare(b.cells[n].textContent.trim());
            return c > 0 ? 1 : (c < 0 ? -1 : 0) }
    }
    var isSorted = function(array, fn) {
        if (array.length < 2)
            return 1;
        var direction = fn(array[0], array[1]);
        for (var i = 1; i < array.length - 1; ++i) {
            var d = fn(array[i], array[i+1]);
            if (d == 0)
                continue;
            else if (direction == 0)
                direction = d;
            else if (direction != d)
                return 0;
            }
        return direction;
    }
    var sorted = isSorted(tr, fn);
    if (sorted == 1 || sorted == -1) {
        // if sorted already, reverse it
        for(var i = tr.length - 1; i >= 0; --i)
            tb.appendChild(tr[i]); // append each row in order
    } else {
        tr = tr.sort(fn);
        for(var i = 0; i < tr.length; ++i)
            tb.appendChild(tr[i]); // append each row in order
    }
}
</script>

%(panel)s

%(active_page)s

<div class="container-fluid main-container">

<!-- tabsets -->
<script src="../site_libs/navigation-1.1/tabsets.js"></script>
<script>
    $(document).ready(function () {
      window.buildTabsets("TOC");
    });
</script>

%(header)s

<title>%(name)s | REPLACEMETITLE</title>

<style type = "text/css">
    body {
      %(font)s
    }
</style>
</head>

<body>
<div tabindex="-1" id="notebook" class="border-box-sizing">
<div class="container" id="notebook-container">

<!-- code folding -->

%(navbar)s

%(panel)s
{%%- endblock header -%%}
%(body)s
{%% block footer %%}
<hr>
%(footer)s
</div>
</div>
</body>

%(pandoc_to_bs4)s

<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=UA-9902895-3"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'UA-9902895-3');
</script>

</html>
{%% endblock %%}
''' % {
        'version': conf['__version__'],
        'common_style': get_common_stylesheets(),
        'user_style':
            '<link rel="stylesheet" type="text/css" href="../css/%s.css">' % conf['jt_theme']
            if conf['jt_theme'] is not None else '',
        'common_javascript': get_common_javascript(),
        'highlightjs_init': get_highlightjs_init(),
        'mathjax_init': get_mathjax_init(),
        'sidebar': get_sidebar(path) if conf['notebook_toc'] else '',
        'header': get_sos_tpl('header' if conf['report_style'] is True else ''),
        'font': get_font(conf['font']),
        'name': conf['name'],
        'active_page': get_active_page(),
        'pandoc_to_bs4': convert_pandoc_to_bs4(),
        'navbar': get_navbar(conf['name'],
                             get_nav([x for x in dirs if x not in conf['hide_navbar']],
                                     conf['homepage_label'], '../'),
                             get_right_nav(conf['repo'], conf['source_label'])),
        'panel': get_sos_tpl('panel' if conf['report_style'] is True else ''),
        'body': get_sos_tpl('body' if conf['report_style'] is True else ''),
        'footer': conf['footer']
    }
    return content


def update_gitignore():
    flag = True
    if os.path.isfile('.gitignore'):
        lines = [x.strip() for x in open('.gitignore').readlines()]
        if '**/.sos' in lines:
            flag = False
    if flag:
        with open('.gitignore', 'a') as f:
            f.write('\n**/.sos\n**/.ipynb_checkpoints\n**/__pycache__')


def make_template(conf, dirs, outdir):
    with open('{}/index.tpl'.format(outdir), 'w') as f:
        f.write(get_index_tpl(conf, dirs).strip())
    for item in dirs:
        with open('{}/{}.tpl'.format(outdir, item), 'w') as f:
            f.write(get_notebook_tpl(conf, dirs, item).strip())


def get_notebook_toc(path, exclude):
    map1 = dict()
    map2 = dict()
    for fn in sorted(glob(os.path.join(path, "*.ipynb"))):
        if os.path.basename(fn) in ['_index.ipynb', 'index.ipynb'] or fn in exclude:
            continue
        name = os.path.basename(fn[:-6]).strip()
        with open(fn) as f:
            data = json.load(f)
        try:
            idx = 0
            while True:
                title = data["cells"][0]["source"][idx].strip()
                if title:
                    break
                idx += 1
        except IndexError:
            title = name
            continue
        #  FIXME: this regex is to be continuously updated based on observed TOC generated
        map2[name] = short_repr(title.replace('`', '').strip('#').strip())[1:-1]
        title = re.sub('[^0-9a-zA-Z-:&!?@.,()+]+', '-', title).strip('-') + "-1"
        map1[title] = name
    out = f"var {os.path.basename(path)}Dict = {str(map1)}\n"
    out += f"var {os.path.basename(path)}ArrayMap = {str(map2)}"
    return out


def get_index_toc(path):
    out = f'var {os.path.basename(path)}Array = '
    # Reference index
    fr = os.path.join(path, '_index.ipynb')
    if not os.path.isfile(fr):
        return out + '[]'
    # Actual index
    fi = os.path.join(path, 'index.ipynb')
    if not os.path.isfile(fi):
        fi = fr
    # Collect HTML file names from index file
    res = []
    with open(fi) as f:
        data = json.load(f)
    for cell in data['cells']:
        for sentence in cell["source"]:
            doc = re.search(r'^.*\/(.+?).html', sentence)
            if doc:
                res.append(doc.group(1))
    # Filter by reference index
    if not fi == fr:
        ref = []
        with open(fr) as f:
            data = json.load(f)
        for cell in data['cells']:
            for sentence in cell["source"]:
                doc = re.search(r'^.*\/(.+?).html', sentence)
                if doc:
                    ref.append(doc.group(1))
        res = [x for x in res if x in ref]
    return out + repr(res)


def get_toc(path, exclude):
    return [get_index_toc(path) + '\n' + get_notebook_toc(path, exclude)]


def make_index_nb(path, exclude, long_description=False, reverse_alphabet=False):
    sos_files = [x for x in sorted(glob(os.path.join(path, "*.sos")),
                                   reverse=reverse_alphabet) if x not in exclude]
    out = '''
{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# %s"
   ]
  },''' % os.path.basename(path).replace('_', ' ').capitalize()
    if len(sos_files):
        out += '''
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Notebooks"
   ]
  },'''
    date_section = None
    add_date_section = False
    for fn in sorted(glob(os.path.join(path, "*.ipynb")), reverse=reverse_alphabet):
        if os.path.basename(fn) in ['_index.ipynb', 'index.ipynb'] or fn in exclude:
            continue
        name = os.path.splitext(os.path.basename(fn))[0].replace('_', ' ')
        tmp = "{}/{}".format(name[:4], name[4:6])
        if is_date(tmp) and date_section != tmp:
            date_section = tmp
            add_date_section = True
        with open(fn) as f:
            data = json.load(f)
        try:
            source = [x.strip() for x in data["cells"][0]["source"] if x.strip()]
            if long_description\
               and source[0].startswith('#')\
               and len(source) >= 2\
               and not source[1].startswith('#'):
                title = source[0].lstrip('#').strip()
                description = source[1].lstrip('#').strip()
            else:
                title = name.strip()
                description = source[0].lstrip('#').strip()
        except IndexError:
            continue
        if add_date_section:
            add_date_section = False
            out += '''
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### %s\\n"
   ]
  },''' % date_section
        html_link = (os.path.splitext(os.path.basename(fn))[0] + '.html')\
            if os.path.splitext(os.path.basename(fn))[0] != os.path.basename(os.path.dirname(fn))\
            else 'index.html'
        if title != description:
            out += '''
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "[**%s**](%s/%s)<br>\\n",
    %s
   ]
  },''' % (title, path, html_link, json.dumps("&nbsp; &nbsp;" + description))
        else:
            out += '''
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "[**%s**](%s/%s)<br>"
   ]
  },''' % (title, path, html_link)
    if len(sos_files):
        out += '''
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Pipelines"
   ]
  },'''
    for fn in sos_files:
        name = os.path.splitext(os.path.basename(fn))[0].replace('_', ' ')
        out += '''
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "[%s](%s/%s)"
   ]
  },''' % (name, path, os.path.splitext(os.path.basename(fn))[0] + '.pipeline.html')
    out = out.strip(',') + '''
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}'''
    return out.strip()


def make_empty_nb(name):
    return '''{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Welcome to %s!"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}''' % name


def protect_page(page, page_tpl, password, write):
    # page: docs/{name}
    page_dir, page_file = os.path.split(page)
    page_file = '/'.join(page.split('/')[1:])
    secret = page_dir + '/' + sha1((password + page_file).encode()).hexdigest() + '.html'
    if write:
        content = open(page).readlines()
        content.insert(5, '<meta name="robots" content="noindex">\n')
        with open(secret, 'w') as f:
            f.write(''.join(content))
        content = open(page_tpl).readlines()
        with open(page, 'w') as f:
            f.write(''.join(content).replace("TPL_PLACEHOLDER", page_file))
    secret = os.path.basename(secret)
    return secret, f'docs/{secret.rsplit(".", 1)[0]}_{os.path.basename(page_dir)}.sha1'


def get_sha1_files(index_files, notebook_files, passwords, write=False):
    # Inputs are list of files [(input, output), ...]
    password = [None if passwords is None or (os.path.dirname(fn[0]) not in passwords and fn[0] not in passwords) else (passwords[os.path.dirname(fn[0]) if (os.path.dirname(fn[0]) in passwords and not fn[0] in passwords) else fn[0]]) for fn in index_files] + [None if passwords is None or fn[0] not in passwords else passwords[fn[0]] for fn in notebook_files]
    res = [protect_page(fn[1], 'docs/site_libs/jnbinder_password.html', p, write)[1]
           for fn, p in zip(index_files + notebook_files, password) if p]
    return res
