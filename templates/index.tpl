% setdefault('show', 'all')
% setdefault('nr', 1)
<div id = 'filter' class="well" style="padding: 8px 0;">
    <ul class="nav nav-list">
        <li class="nav-header">Show What ?</li>
    % for s in ('all', 'critical', ):
        % if s == show:
        <li class="active"><a href="/index?show={{s}}">{{s}}</a></li>
        % else:
        <li><a href="/index?show={{s}}">{{s}}</a></li>
        % end
    % end
        <li class="divider"></li>
        <li><a href="https://github.com/huoxy/graphite-alerter">@Github</a></li>
    </ul>
</div>
<div id = 'info'>
    <table class = 'table table-bordered table-striped table-hover'>
        <thead>
            <tr>
                <th>#</th>
                <th>Metric Name</th>
                <th>Current Value</th>
                <th>Max Value</th>
                <th>Min Value</th>
                <th>Last Update</th>
                <th>Retrys</th>
                <th></th>
            </tr>
        </thead>
        <tbody>
        % for plugin in plugins:
            % for target in plugin.targets:
                % for metric in target.metrics:
                    % if show == 'all' or (show == 'critical' and metric.retry):
                    % retry = metric.retry
            <tr>
                <td>{{nr}}</td>
                <td>{{metric.name}}</td>
                <td>{{metric.curr}}</td>
                <td>{{target.max}}</td>
                <td>{{target.min}}</td>
                        % import datetime
                <td>{{datetime.datetime.fromtimestamp(int(metric.last_update)).strftime('%H:%M:%S / %d')}}</td>
                    % if retry == 0:
                        % c = 'label label-success'
                    % else:
                        % c = 'label label-important'
                    % end
                <td><span class = '{{c}}'>{{retry}} / {{target.retry}}</span></td>
                    % if retry == 0:
                <td></td>
                    % end
                    % if retry > 0 and not metric.ack:
                <td><a class = 'btn btn-small' href = '/ack/{{metric.name}}'>Ack</a></td>
                    % end
                    % if retry > 0 and metric.ack:
                <td><a class = 'btn btn-small disabled' href = '{{metric.name}}'>Ack-ed</a></td>
                    % end
            </tr>
                        % nr += 1
                    % end
                % end
            % end
        % end
        <tbody>
    </table>
</div>
