#!/usr/bin/env python2

import json, urllib2, re
import config


class Metric:

    def __init__(self, name):
        self.name = name
        self.retry = 0

    @property
    def value(self): # return the last point, return -1 if None
        url = '/render/?target=%s&from=-10min&format=json' % (config.graphite_url, self.name)
        val = json.loads(urllib2.urlopen(url))[0]['datapoints'][-1][0]
        return val is None and -1 or val


class Target:
    
    def __init__(self, match, max, min, retry = 3):
        self.match = match
        self.match_obj = re.compile(self.match)
        self.max = max
        self.min = min
        self.retry = retry
        self.metrics = []


class Plugin:
    
    def __init__(self, name):
        self.name = name
        self.targets = []


