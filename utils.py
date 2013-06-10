#!/usr/bin/env python2
import json, logging, urllib2, sys, os, time
from signal import SIGINT

import config
from models import Metric, Target, Plugin


metrics_matched = {}
logging.basicConfig(format = '[%(asctime)s] %(msg)s', level = logging.DEBUG)


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
    global metrics_matched

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
                        if metrics_matched.has_key(m): # won't match twice
                            continue
                        else:
                            metric = Metric(m)
                            metrics_matched[m] = metric
                            t.metrics.append(metric)
                logging.info('   - target: "%s", metrics: %s' % (t.match, len(t.metrics)))

            plugins_.append(plugin)
        except:
            logging.debug(' - ERROR occur when loading plugin [ %s ]' % module)

    return plugins_

def do(msg):
    pass
#    logging.info(' - %s : %s' % (msg['name'], msg['curr']))


def update_metric(metric):
    metric.curr = metric.value
    metric.last_update = time.time()


def signal_handler(signalnum, frame):
    if signalnum == SIGINT:
        logging.info('Graphite Alert Exiting')
        sys.exit(0)


