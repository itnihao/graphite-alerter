#!/usr/bin/env python2

import json, urllib2, re
import config


class Metric:

    def __init__(self, name):
        self.name = name
        self.url = '%s/render/?target=%s&from=-5min&format=json' % (config.graphite_url, self.name)
        self.retry = 0
        self.curr = None
        self.last_update = None

    @property
    def value(self): # return the last point, return -1 if None
        response = urllib2.urlopen(self.url)
        points = [p for p in json.loads(response.read())[0]['datapoints'] if p[0] is not None]
        return points[-1][0] # maybe None


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


