{%- extends 'basic.tpl' -%}

{%- block header -%}
{{ super() }}
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta name="ipynb_website:version" content="0.9.7" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<meta name="twitter:card" content="summary_large_image"></meta>
<meta property="og:title" content="US Macroeconomic Data Explorer | REPLACEMETITLE" />
<meta property="og:type" content="article" />
<meta property="og:description" content="REPLACEMEDESCRIPTION" />
<meta property="og:image" content="REPLACEMEIMAGE" />
<meta property="og:url" content="REPLACEMEURL" />

<!-- begin stylesheets -->

<link rel="stylesheet"
    href="../css/jt.css">
<link rel="stylesheet"
    href="../css/toc2.css">
<link rel="stylesheet"
    href="../site_libs/jqueryui-1.11.4/jquery-ui.css">
<link rel="stylesheet"
    href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
<link rel="stylesheet"
    href="https://cdn.jsdelivr.net/npm/font-awesome@4.7.0/css/font-awesome.min.css">
<link rel="stylesheet"
    href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@9.18.1/build/styles/default.min.css">
    
<link rel="stylesheet" type="text/css" href="../css/readable.css">
<!-- end stylesheets -->

<!-- begin javascript -->

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
<script src="https://cdn.jsdelivr.net/npm/vega@5"></script>
<script src="https://cdn.jsdelivr.net/npm/vega-lite@4"></script>
<script src="https://cdn.jsdelivr.net/npm/vega-embed@6"></script>

<script src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@9.18.1/build/highlight.min.js"></script>

<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.2/MathJax.js?config=TeX-MML-AM_CHTML"></script>
    
<!-- end javascript -->


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
    

<script src="../js/doc_toc.js"></script>
<script src="../js/docs.js"></script>


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
<script src="../site_libs/navigation-1.1/tabsets.js"></script>
<script>
    $(document).ready(function () {
      window.buildTabsets("TOC");
    });
</script>



<title>US Macroeconomic Data Explorer | REPLACEMETITLE</title>

<style type = "text/css">
    body {
      
    }
</style>
</head>

<body>
<div tabindex="-1" id="notebook" class="border-box-sizing">
<div class="container" id="notebook-container">

<!-- code folding -->


<nav class="navbar navbar-expand-lg sticky-top navbar-light bg-light">
    <a class="navbar-brand" href="../index.html">US Macroeconomic Data Explorer</a>
    <button type="button" class="navbar-toggler collapsed" data-toggle="collapse" data-target="#navbar" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div id="navbar" class="navbar-collapse collapse">
      <ul class="navbar-nav mr-auto">
        
<li class="nav-item">
  &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;
</li>
        
<li class="nav-item dropdown">
  <a class="nav-link dropdown-toggle btn" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" style="background-color: steelblue; color: white;">
    Explore other charts
  </a>
  <div class="dropdown-menu" aria-labelledby="navbarDropdown">
  

    <a class="dropdown-item" href="../analysis/autos.html">Autos</a>
        
    <a class="dropdown-item" href="../analysis/construction.html">Construction</a>
        
    <a class="dropdown-item" href="../analysis/creditcards.html">Creditcards</a>
        
    <a class="dropdown-item" href="../analysis/international-trade.html">International Trade</a>
        
    <a class="dropdown-item" href="../analysis/labor.html">Labor</a>
        
    <a class="dropdown-item" href="../analysis/manufacturing.html">Manufacturing</a>
        
    <a class="dropdown-item" href="../analysis/oil-gas-inventories.html">Oil Gas Inventories</a>
        
    <a class="dropdown-item" href="../analysis/residential-realestate-zillow.html">Residential Realestate Zillow</a>
        
    <a class="dropdown-item" href="../analysis/residential-realestate.html">Residential Realestate</a>
        
    <a class="dropdown-item" href="../analysis/retailsales.html">Retailsales</a>
        
    <a class="dropdown-item" href="../analysis/sentiment.html">Sentiment</a>
        
    <a class="dropdown-item" href="../analysis/services.html">Services</a>
        
    <a class="dropdown-item" href="../analysis/sp500-returns-and-performance.html">Sp500 Returns And Performance</a>
        
    <a class="dropdown-item" href="../analysis/transportation-cass.html">Transportation Cass</a>
        
    <a class="dropdown-item" href="../analysis/transportation-ocean.html">Transportation Ocean</a>
        
    <a class="dropdown-item" href="../analysis/transportation-rail.html">Transportation Rail</a>
        
    <a class="dropdown-item" href="../analysis/us-treasury-auctions.html">Us Treasury Auctions</a>
        
    <a class="dropdown-item" href="../analysis/us-treasury-rates.html">Us Treasury Rates</a>
        
  </div>
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
&copy; 2020 pymoment
</div>
</div>
</body>


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
    

<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=UA-9902895-3"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'UA-9902895-3');
</script>

</html>
{% endblock %}