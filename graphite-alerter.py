#!/usr/bin/env python

import time
import threading
from threading import Thread
from collections import deque
from signal import signal, SIGINT

from bottle import route, run, template, static_file, request, redirect

from utils import load_metrics, load_plugins, logging, do, update_metric, signal_handler
from utils import metrics_matched # find metric quickly
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
                        metric.retry = 0
                        metric.ack = None
                    else:
                        if metric.retry < target.retry:
                            metric.retry += 1
                    if metric.retry == 3:
                        messages.append({'name':metric.name, 'value':value})
#                        metric.retry = 0 # re-schedule
        time.sleep(10) # check interval

# alert for each "critical" messages
def alert():

    while True:
        curr_len = len(messages)
        cnt = 0
        if config.debug:
            logging.debug('alerting metrics(%s)...' % curr_len)
        while cnt < curr_len:
            msg = messages.popleft()
            do(msg)
            cnt += 1
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
    if metric_name is None:
        return redirect('/')
    metric = metrics_matched[metric_name]
    metric.ack = True
    return redirect(request.headers.get('Referer', '/'))

@route('<path:re:/static/css/.*css>')
@route('<path:re:/static/js/.*js>')
def static(path, method = 'GET'):
    return static_file(path, root = '.')


## main thread

def main():

    logging.info('Graphite Alert Starting...')

    signal(SIGINT, signal_handler)

    global metrics
    metrics = load_metrics()

    global plugins
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

    while True:
        global ready
        if ready:
            run(host = config.listen_host, port = int(config.listen_port))
        time.sleep(1)


if __name__ == '__main__' :
    main()



