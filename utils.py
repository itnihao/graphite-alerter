#!/usr/bin/env python2
import json, logging, urllib2, sys, os

import config
from models import Metric, Target, Plugin


logging.basicConfig(format = '[%(asctime)s] %(msg)s', level = logging.DEBUG)


def load_metrics():
    try:
        logging.info('Loading metrics...')
        response = urllib2.urlopen("%s/metrics/index.json" % config.graphite_url)
        metrics = json.loads(response.read())
        logging.info(' - %s metrics found' % len(metrics))
        return metrics
    except:
        logging.info('Loading metrics error, exit')
        sys.exit(1)


def load_plugins(metrics = None):
    import plugins

    plugins_ = []

    plugins_dir = os.path.dirname(plugins.__file__)

    logging.info('Loading plugins...')
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
                        t.metrics.append(Metric(t))
                logging.info('   - target: "%s", metrics: %s' % (t.match, len(t.metrics)))
            plugins_.append(plugin)


        except:
            logging.info(' - ERROR occur when loading plugin [ %s ]' % module)


    return plugins_
