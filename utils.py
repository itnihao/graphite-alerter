#!/usr/bin/env python2
import json, logging, urllib2, sys, os, time, pickle
from signal import SIGINT

import config
from models import Metric, Target, Plugin


logging.basicConfig(format = '[%(asctime)s] %(msg)s', level = logging.DEBUG)


def find_metric(plugins, name):
    for plugin in plugins:
        for target in plugin.targets:
            for metric in target.metrics:
                if metric.name == name:
                    return metric
    return None


def load_metrics():
    try:
        logging.debug('Loading metrics...')
        response = urllib2.urlopen("%s/metrics/index.json" % config.graphite_url)
        metrics = json.loads(response.read())
        logging.info(' - %s metrics' % len(metrics))

        return metrics
    except:
        logging.debug('Loading metrics error, exit')
        sys.exit(1)


def load_plugins(metrics = None):
    import plugins

    plugins_ = []

    plugins_dir = os.path.dirname(plugins.__file__)

    logging.debug('Loading plugins...')
    for f in os.listdir(plugins_dir):
        if f == '__init__.py' or not f.endswith(".py"):
            continue
        try:
            name = f[:-3]
            imp = __import__('plugins.' + name, globals(), locals(), ['*'])
            assert(hasattr(imp, 'targets'))
            plugin = Plugin(name)

            logging.info(' - plugin [%s]' % name)
            for t in imp.targets:
                plugin.targets.append(Target(**t))

            for t in plugin.targets:
                for m in metrics:
                    if t.match_obj.match(m):
                        if find_metric(plugins_, m): # won't match twice
                            continue
                        else:
                            metric = Metric(m)
                            t.metrics.append(metric)
                logging.info('   - target: "%s", metrics: %s' % (t.match, len(t.metrics)))

            plugins_.append(plugin)
        except:
            logging.debug('ERROR: Loading plugins [ %s ]' % module)

    return plugins_

def load_plugins_from_cache():
    try:
        logging.info('Loading plugins from cache...')
        return pickle.loads(open(config.plugins_cache, 'rb').read())
    except:
        logging.info(' - Error: Loading plugins from cache...')
        raise

def do(msg):
    pass
#    logging.info(' - %s : %s' % (msg['name'], msg['curr']))


def update_metric(metric):
    metric.value = metric.curr
    metric.last_update = time.time()


def reset(metric):
    metric.retry = 0
    metric.ack = None


def signal_handler(signalnum, frame):
    if signalnum == SIGINT:
        logging.info('Graphite Alert Exiting...')
        sys.exit(0)


def deepcopy(plugins):
    return pickle.loads(pickle.dumps(plugins))


def readable(num):
    for x in ['','K','M','G']:
        if num < 1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0
    return "%3.1f%s" % (num, 'T')
