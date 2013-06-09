#!/usr/bin/env python

import time
import threading
from threading import Thread
from utils import load_metrics, load_plugins, logging, do

import schedule

metrics = plugins = None

def fetch():

    global plugins
    for plugin in plugins:
        for target in plugin.targets:
            for metric in target.metrics:
                metric.curr = metric.value
    logging.info('refreshing metrics...')


def check(plugin):

    while True:
        for target in plugin.targets:
            for metric in target.metrics:
#                logging.info('[%s] [%s]' % (threading.current_thread().name, metric.name))
                if target.min <= metric.curr <= target.max:
                    metric.retry = 0
                else:
                    metric.retry += 1
                if metric.retry == 3:
                    do(plugin, target, metric)
                    metric.retry = 0 # re-schedule
        time.sleep(5)


def main():

    global metrics
    metrics = load_metrics()

    global plugins
    plugins = load_plugins(metrics)

    fetch() # fetch first

    for plugin in plugins:
        t = Thread(target = check, args = (plugin, ))
        t.setDaemon(True)
        t.start()

    # always infinitely
    schedule.every(10).seconds.do(fetch)
    while True:
        schedule.run_pending()
        time.sleep(1)

main()



