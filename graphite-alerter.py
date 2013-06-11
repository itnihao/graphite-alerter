#!/usr/bin/env python

import time, os, threading, pickle
from threading import Thread
from collections import deque
from signal import signal, SIGINT

from bottle import route, run, template, static_file, request, redirect

from utils import load_metrics, load_plugins, load_plugins_from_cache, logging, do, \
    update_metric, signal_handler, reset, find_metric
import config

metrics = plugins = None
messages = deque()
ready = False


## 3 daemons

 # fetch each metric value
def fetch():

    global ready
    global plugins
    while True:
        if config.debug:
            logging.debug('fetching metrics...')
        for plugin in plugins:
            for target in plugin.targets:
                for metric in target.metrics:
                    update_metric(metric)
        ready = True
        time.sleep(10)

 # check each metrics and update retry ...
def check():

    while True:
        if config.debug:
            logging.debug('checking metrics...')
        for plugin in plugins:
            for target in plugin.targets:
                for metric in target.metrics:
                    if metric.value is None:
                        update_metric(metric)
                    value = metric.value
                    if target.min <= value <= target.max:
                        reset(metric)
                    else:
                        if metric.retry < target.retry:
                            metric.retry += 1
                    if metric.retry == 3:
                        messages.append({'name':metric.name, 'value':value})
#                        metric.retry = 0 # re-schedule
        time.sleep(10) # check interval

# alert for each "critical" messages
def alert():

    global messages
    while True:
        curr_len = len(messages)
        cnt = 0
        if config.debug:
            logging.debug('alerting metrics...(%s messages)' % curr_len)
        while cnt < curr_len:
            msg = messages.popleft()
            do(msg)
            cnt += 1
        time.sleep(10)

# cache "plugins"
def cache():

    global plugins
    global ready
    while True:
        if ready:
            if config.debug:
                logging.info('cacheing plugins...')
            tempfile = config.plugins_cache + '.tmp'
            try:
                open(tempfile, 'wb').write(pickle.dumps(plugins))
                os.rename(tempfile, config.plugins_cache)
            except:
                logging.info('Error: cache plugins')
        time.sleep(10)

## web

def render_page(body, page = 'index'):
    return str(template('templates/base', body = body, page = page))

@route('/')
@route('/index')
def index():
    global plugins
    show = request.query.get('show', 'all')
    body = template('templates/index' , plugins = plugins, show = show)
    return render_page(body)

@route('/ack/<metric_name>')
def ack(metric_name = None):
    global plugins
    if metric_name is None:
        return redirect('/')
    metric = find_metric(plugins, metric_name)
    metric.ack = True
    return redirect(request.headers.get('Referer', '/'))

@route('/debug', method = 'GET')
def debug():
    body = template('templates/debug' , plugins = plugins)
    return render_page(body, page = 'debug')

@route('<path:re:/static/css/.*css>')
@route('<path:re:/static/js/.*js>')
def static(path, method = 'GET'):
    return static_file(path, root = '.')


## main thread

def main():

    app_dir = os.path.dirname(__file__)
    if app_dir:
        os.chdir(app_dir)

    logging.info('Graphite Alert Starting...')

    signal(SIGINT, signal_handler)

    global metrics
    metrics = load_metrics()

    global plugins
    try:
        plugins = load_plugins_from_cache()
    except:
        plugins = load_plugins(metrics)

    # start fetch
    t = Thread(target = fetch)
    t.setDaemon(True)
    t.start()

    # start check
    t = Thread(target = check)
    t.setDaemon(True)
    t.start()

    # start alert
    t = Thread(target = alert)
    t.setDaemon(True)
    t.start()

    # start dumps
    t = Thread(target = cache)
    t.setDaemon(True)
    t.start()

    while True:
        global ready
        if ready:
            run(host = config.listen_host, port = int(config.listen_port))
        time.sleep(1)


if __name__ == '__main__' :
    main()



