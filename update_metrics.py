#!/usr/bin/env python2
try:
    import json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        raise ImportError("GE requires python2, 2.6 or higher, or 2.5 with simplejson.")
import os
import re

import config

import urllib2
response = urllib2.urlopen("%s/metrics/index.json" % config.graphite_url)
m = open('%s.tmp' % config.filename_metrics, 'w')
m.write(response.read())
m.close()
os.rename('%s.tmp' % config.filename_metrics, config.filename_metrics)

