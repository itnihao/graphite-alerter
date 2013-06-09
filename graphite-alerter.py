#!/usr/bin/env python

from utils import load_metrics, load_plugins, logging

metrics = []
plugins = []

def main():

    global metrics
    metrics = load_metrics()

    global plugins
    plugins = load_plugins(metrics)


main()
