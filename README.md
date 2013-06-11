# Graphite Alerter
Alerter system like nagios

# Screenshot
* /index
![Screenshot](https://raw.github.com/huoxy/graphite-alerter/master/static/image/indexScreenshot.png)
* /debug
![Screenshot](https://raw.github.com/huoxy/graphite-alerter/master/static/image/debugScreenshot.png)

# Plugin
TODO

# Configuration
```python
graphite_url = 'http://<ip>:<port>'
listen_host = '0.0.0.0'
listen_port = 8081
plugins_cache = 'plugins.cache'
debug = False
```
set your own `graphite_url`

# Running
After cloning code:
```bash
cd graphite-alerter
./graphite-alerter.py
```
then you will get your page on: `http://<ip>:8081/`

# Debug
on /debug you will see all plugins details and all metrics matched; or edit config.py, set `debug = True`.
