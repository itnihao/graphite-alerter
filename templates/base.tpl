% setdefault('page', 'index')
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Graphite Alerter</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">

    <link href="/static/css/bootstrap.css" rel="stylesheet">
    <link href="/static/css/graphite-alerter.css" rel="stylesheet">
    <script src="/static/js/jquery.min.js"></script>
  </head>

  <body>
    <div class="navbar navbar-fixed-top">
      <div class="navbar-inner">
        <div class="container-fluid">
          <a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </a>
          <a class="brand" href="/index">Graphite Alerter</a>
          <div class="nav-collapse">
            <ul class="nav">
	% for (key, title) in [('index', 'Home'), ('debug', 'Debug')]:
		% if page == key:
              <li class="active"><a href="/{{key}}">{{title}}</a></li>
		% else:
              <li><a href="/{{key}}">{{title}}</a></li>
		% end
	% end
            </ul>
          </div><!--/.nav-collapse -->
            <ul class="nav pull-right">
            % import time
            <li><a id = 'tip'>{{time.asctime()}}</a> </li>
            </ul>
        </div>
      </div>
    </div>
    <div id = 'content' style = 'margin-left: 20px;'>
    {{!body}}
    </div>
  </body>
</html>
