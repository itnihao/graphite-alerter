#!/usr/bin/env python

import time
import threading
from threading import Thread
from collections import deque
from utils import load_metrics, load_plugins, logging, do

from bottle import route, run, template, static_file, default_app, request

metrics = plugins = None

messages = deque()


## 3 daemons

 # fetch each metric value
def fetch():

    global plugins
    while True:
        for plugin in plugins:
            for target in plugin.targets:
                for metric in target.metrics:
                    metric.curr = metric.value
        logging.info('fetching metrics...')
        time.sleep(10)

 # check each metrics and update retry ...
def check():

    while True:
        logging.info('checking metrics...')
        for plugin in plugins:
            for target in plugin.targets:
                for metric in target.metrics:
    #                logging.info('[%s] [%s]' % (threading.current_thread().name, metric.name))
                    if metric.curr is None:
                        metric.curr = metric.value
                    curr = metric.curr
                    if target.min <= curr <= target.max:
                        metric.retry = 0
                    else:
                        if metric.retry < target.retry:
                            metric.retry += 1
                    if metric.retry == 3:
                        messages.append({'name':metric.name, 'curr':curr})
#                        metric.retry = 0 # re-schedule
        time.sleep(10) # check interval

# alert for each "critical" messages
def alert():

    while True:
        curr_len = len(messages)
        cnt = 0
        logging.info('alerting metrics(%s)...' % curr_len)
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

@route('<path:re:/static/css/.*css>')
@route('<path:re:/static/js/.*js>')
def static(path, method = 'GET'):
    return static_file(path, root = '.')


## main thread

def main():

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

    run(host = '0.0.0.0', port = 8080)


if __name__ == '__main__' :
    main()



