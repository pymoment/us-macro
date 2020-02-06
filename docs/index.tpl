{%- extends 'basic.tpl' -%}

{%- block header -%}
{{ super() }}

<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta name="ipynb_website:version" content="0.9.7" />
<meta name="viewport" content="width=device-width, initial-scale=1" />

<title>US Macroeconomic Data Explorer</title>


<link rel="stylesheet"
    href="css/jt.css">
<link rel="stylesheet"
    href="css/toc2.css">
<link rel="stylesheet"
    href="site_libs/jqueryui-1.11.4/jquery-ui.css">
<link rel="stylesheet"
    href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
<link rel="stylesheet"
    href="https://cdn.jsdelivr.net/npm/font-awesome@4.7.0/css/font-awesome.min.css">
<link rel="stylesheet"
    href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@9.18.1/build/styles/default.min.css">
    

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


<script>
    MathJax.Hub.Config({
        extensions: ["tex2jax.js"],
        jax: ["input/TeX", "output/HTML-CSS"],
        tex2jax: {
            inlineMath: [ ['$','$'], ["\\(","\\)"] ],
            displayMath: [ ['$$','$$'], ["\\[","\\]"] ],
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
      max-width:100%;
      height: auto;
    }
    .tabbed-pane {
      padding-top: 12px;
    }
    button.code-folding-btn:focus {
      outline: none;
    }
</style>


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
    

<div class="container-fluid main-container">

<!-- tabsets -->
<script src="site_libs/navigation-1.1/tabsets.js"></script>
<script>
$(document).ready(function () {
  window.buildTabsets("TOC");
});
</script>

<!-- code folding -->


<nav class="navbar navbar-expand-lg navbar-light bg-light">
    <a class="navbar-brand" href="../index.html">US Macroeconomic Data Explorer</a>
    <button type="button" class="navbar-toggler collapsed" data-toggle="collapse" data-target="#navbar" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div id="navbar" class="navbar-collapse collapse">
      <ul class="navbar-nav mr-auto">
        
<li class="nav-item">
  <a class="nav-link" href="./index.html">Overview</a>
</li>
        
      </ul>
        
<ul class="navbar-nav">
<li class="nav-item">
   <a class="nav-link" href="http://github.com/kdunn926/us-macro"> source </a>
</li>
</ul>
        
    </div><!--/.nav-collapse -->
</nav><!--/.navbar -->
    

{%- endblock header -%}
{% block footer %}
<hr>
&copy; 2020 Kyle Dunn
<!-- To enable disqus, uncomment the section below and provide your disqus_shortname -->

</div>


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
    

<!-- dynamically load mathjax for compatibility with self-contained -->
<script>
  (function () {
    var script = document.createElement("script");
    script.type = "text/javascript";
    script.src  = "https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.2/MathJax.js?config=TeX-MML-AM_CHTML";
    document.getElementsByTagName("head")[0].appendChild(script);
  })();
</script>

</body>
</html>
{% endblock %}