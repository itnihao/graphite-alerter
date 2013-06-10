#!/usr/bin/env python

import time
import threading
from threading import Thread
from collections import deque
from utils import load_metrics, load_plugins, logging, do

import schedule

metrics = plugins = None

messages = deque()

def fetch():

    global plugins
    for plugin in plugins:
        for target in plugin.targets:
            for metric in target.metrics:
                metric.curr = metric.value
    logging.info('fetching metrics...')


def check():

    while True:
        logging.info('checking metrics...')
        for plugin in plugins:
            for target in plugin.targets:
                for metric in target.metrics:
    #                logging.info('[%s] [%s]' % (threading.current_thread().name, metric.name))
                    curr = metric.curr
                    if target.min <= curr <= target.max:
                        metric.retry = 0
                    else:
                        metric.retry += 1
                    if metric.retry == 3:
                        messages.append({'name':metric.name, 'curr':curr})
                        metric.retry = 0 # re-schedule
        time.sleep(20) # check interval


def alert():
    while True:
        logging.info('alerting metrics...')
        try:
            msg = messages.popleft()
            do(msg)
        except IndexError:
            return


def main():

    global metrics
    metrics = load_metrics()

    global plugins
    plugins = load_plugins(metrics)

    fetch() # fetch once

    # start fetch
    t = Thread(target = fetch)
    t.setDaemon(True)
    t.start()

    # start check
    t = Thread(target = check)
    t.setDaemon(True)
    t.start()

    # always infinitely
    schedule.every(10).seconds.do(alert)
    while True:
        schedule.run_pending()
        time.sleep(1)

main()



