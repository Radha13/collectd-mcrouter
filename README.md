# collectd-mcrouter
A [collectd](http://collectd.org/) plugin that collects metrics from [Mcrouter](https://github.com/facebook/mcrouter) stats file. 
It runs under collectd [Python plugin](http://collectd.org/documentation/manpages/collectd-python.5.shtml).

McRouter automatically creates and updates several files useful to monitor it's state, which is by default created under [`/var/mcrouter/stats`](https://github.com/facebook/mcrouter/wiki/Stats-files).
More information on stats list [here](https://github.com/facebook/mcrouter/wiki/Stats-list).
## Requirements

* collectd 4.9 or later (for the Python plugin)
* Python 2.6 or later

## Install

1. Clone this repository somewhere accessible by collectd, e.g `/usr/share/collectd/collectd-mcrouter`.
1. Create a collectd configuration file for the plugin preferably in `/etc/collectd/managed_config/` (see the example below).
1. Restart collectd.

## Sample configuration

```
<LoadPlugin python>
        Globals true
</LoadPlugin>

<Plugin python>
        # mcrouter_stats.py is at "/usr/share/collectd/collectd-mcrouter/mcrouter_stats.py"
        ModulePath "/usr/share/collectd/collectd-mcrouter"
        LogTraces true
        Interactive false
        Import "mcrouter_stats"
        <Module "mcrouter_stats">
                Port <mcrouter_port_number>
                # McRouter exposes metrics in "/var/mcrouter/stats"
                DataDir "/path/to/mcrouter/stats/file"
        </Module>
</Plugin>
```
### Dashboard
* Gets per second
![gets per second](dashboard/gets_per_second.png)

* Sets since process start
![sets since start](dashboard/sets_since_start.png)
