#!/usr/bin/python

# McRouter-collectd-plugin - mcrouter_stats.py
#
# Author: Radha Kumari <rkumari@slack-corp.com>
# Organization: Slack Inc.
# Description: This is a collectd plugin that runs under python plugin and
# reads stats exposed by McRouter.
#
# Plugin structure taken from
# https://github.com/salesforce/LinuxTelemetry/blob/master/plugins/netstats.py

import os
import collectd
import json
import platform
import socket

os_name = platform.system()
host_name = socket.gethostname()

MCROUTER_STATS_FNAME = ''
METRIC_PLUGIN = 'mcrouter_stats'
METRIC_TYPE = 'gauge'


def read_mcrouter_stats():
    """
        Reads metrics from mcrouter and dispatches them to collectd as (key, value) pair.
    """
    stats_hash = {}
    if not os.path.exists(MCROUTER_STATS_FNAME):
        collectd.error('mcrouter_stats: path %s does not exist' %
                       (MCROUTER_STATS_FNAME))
        return
    try:
        with open(MCROUTER_STATS_FNAME) as f:
            content = json.load(f)
            stats_hash = {key.split(".")[-1]: content[key] for key in content}
    except IOError as e:
        collectd.error("ERROR: Unable to open the stats file", e)
        return
    except ValueError as e:
        collectd.error('ERROR: Invalid json data', e)
        return
    except Exception as e:
        collectd.error("Something went wrong while reading stats file", e)
        return

    for key, value in stats_hash.items():
        dispatch_metrics(key, value)


def dispatch_metrics(key, value):
    metric = collectd.Values()
    metric.host = host_name
    metric.plugin = METRIC_PLUGIN
    metric.type = METRIC_TYPE
    metric.values = [value]
    metric.type_instance = key
    collectd.debug('key: %s , value: %s' % (key, value))
    metric.dispatch()


def configure_plugin(conf):
    """
        A callback method that loads information (port and stats file path as DataDir)
        from the McRouter collectd plugin config file.
    """
    port = ''
    datadir = ''
    global MCROUTER_STATS_FNAME
    collectd.info('mcrouter stats plugin: configuring host: %s' % (host_name))
    for node in conf.children:
        if node.key == 'Port':
            try:
                port = int(node.values[0])
            except TypeError:
                collectd.error('Error: Port parameter should be an integer!')
                return
        elif node.key == 'DataDir':
            datadir = node.values[0]
        else:
            collectd.warning('mcrouter_stats plugin: unknown key: %s' % node.key)
    MCROUTER_STATS_FNAME = ('%slibmcrouter.mcrouter.%s.stats' % (datadir, port))
    collectd.info('Plugin configured for mcrouter port: %s, mcrouter stats file path: %s' % (port, datadir))


def shutdown():
    collectd.info("mcrouter_stats plugin shutting down")


if os_name == 'Linux':
    collectd.register_config(configure_plugin)
    collectd.register_read(read_mcrouter_stats)
    collectd.register_shutdown(shutdown)
else:
    collectd.warning('mcrouter stats plugin currently works for Linux only')
