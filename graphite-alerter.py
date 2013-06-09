#!/usr/bin/env python

import time
from utils import load_metrics, load_plugins, logging

metrics = plugins = None

def checker(plugin):

    while True:
        for t in plugin.targets:
            for m in t.metrics:
                curr = m.value
                logging.info('[%s] %s: %s < %s < %s' % (plugin.name, m.name, t.min, curr, t.max))
                if t.min <= curr <= t.max:
                    m.retry = 0
                else:
                    m.retry += 1
#                if m.retry == 3:
#                    logging.info('[%s] %s: %s < %s < %s is False' % \
#                        (plugin.name, m.name, t.min, curr, t.max))
        time.sleep(1)


def main():

    global metrics
    metrics = load_metrics()

    global plugins
    plugins = load_plugins(metrics)

    p = plugins[0]


    checker(p)


main()
