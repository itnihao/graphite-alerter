% setdefault('nr', 1)
<div id = 'debug'>
    <table class = 'table table-bordered table-striped table-hover'>
        <thead>
            <tr>
                <th>#</th>
                <th>Plugin Name</th>
                <th>Target</th>
                <th>Metric Name</th>
                <th>Max Value</th>
                <th>Min Value</th>
                <th>Max Retry</th>
            </tr>
        </thead>
        <tbody>
% for plugin in plugins:
    % for target in plugin.targets:
        % for metric in target.metrics:
            <tr>
                <td>{{nr}}</td>
                <td>{{plugin.name}}</td>
                <td>{{target.match}}</td>
                <td>{{metric.name}}</td>
                <td>{{target.max}}</td>
                <td>{{target.min}}</td>
                <td>{{target.retry}}</td>
            </tr>
            % nr += 1
        % end
    % end
% end
        <tbody>
    </table>
    <script>
    </script>
</div>
