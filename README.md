# Dynatrace-Generic-Execution-Plugin
A Sample OneAgent Plugin that collects additional metrics for the host it is deployed on by executing configurable commands

## Motivation for this project
The entities (hosts, processes, ...) in your environment, that are monitored by Dynatrace, ususally offer many more metrics than the Dynatrace OneAgent is collecting out of the box.

Specifically for host metrics it's very often just a matter of invoking an already existing utility on the command line that provides these metrics.

This Plugin allows you to specify and configure these additional metrics within the `plugin.json` file alongside with the command line to invoke and a regular expression that extracts the timeseries data from the output delivered by this command.
There is no need to modify the Python Code of the Plugin, unless you would like to extend it with additional functionality.

This project is meant to serve as a template for situations where there already exists an executable command, that is able to gather data in an easier fashion than implementing that functionality within Python completely. It's nevertheless in general advisable to find ways to query for the same data from within Python without having to invoke an external process - most apparent reason for that is a better chance for proper error handling.

## Installation
OneAgent Plugins need to get installed both, on your Tenant and on the host(s) they are supposed to collect data for - mainly for security reasons. NO third party code is getting executed by your OneAgent unless your Tenant and your Agent agree on the authenticity of your plugin.
This is why you need to install any custom plugin, in addition to your Tenant, on selected Hosts, that have OneAgent running and are supposed to execute your plugin.
### Installation on your Dynatrace Tenant
* Package the file `plugin.json` and `gen_exec_plugin.py` into a zip archive named `custom.python.generic_exec_plugin.zip`.
* Navigate in the Web Interface of your Tenant to `Settings / Monitoring / Monitored Technologies` and select the tab `Custom Plugins`.
* Click on the button `Upload Plugin` and install your zip archive on your tenant.
* Select the new entry in the list of your plugins and promote it from Staging to Production
### Installation on your monitored host
* Make sure you're installing this Plugin on a Linux host. Without any modifications it won't produce valid results on Windows.
* Create a folder name `custom.python.generic_exec_plugin` within `/opt/dynatrace/oneagent/plugin_deployment`
* Copy `plugin.json` and `gen_exec_plugin.py` into that folder
* Restart Oneagent (e.g. `sudo service oneagent restart`)
* Make sure that the configured executable(s) exist and can get executed. For the sample configuration a shell script like this should be sufficient.
```console
#!/bin/sh
ls -f . | wc -l
```
### Troubleshooting
* The unmodified `plugin.json` expects an executable or shell script to be located at `/home/<user>/listfiles`.
* Did you adapt the location of that file?
* Check the permissions for this file. Is it executable for the user your Plugin Agent is executed for? (usually `dtuser`)
* The Python code of the out of the box Plugin evaluates just the first line of the output written by `/home/<user>/listfiles` to stdout.
* You may have to extend the Python code in case you'd like to parse multiple lines.
* Especially when testing out the Plugin on a fresh Linux installation it's likely that the Plugin Agent doesn't seem to see the host to match the requirements for executing the Plugin at all. Reason for that is, that the Plugin Engine primarily focuses on the existence of processes that match the configured criteria. If there doesn't exist at least one process that is considered by OneAgent to be worth monitoring, the Plugin Engine won't execute the Plugin. A feasible workaround here is to install Apache HTTPD on short notice on the development machine (no need for specific confgurations).


## Customization
In this document only the configuration options relevant to this plugin are mentioned.
Customizing the declarative part of a OneAgent Plugin is getting explained in detail within the [OneAgent SDK documentation](https://dynatrace.github.io/plugin-sdk/index.html).

### Metric definition
This Project by default just invokes a sample executable it expects to find on your monitored host.
In order to add more metrics to be captured you will need to modify the `plugin.json` before deploying the Plugin.

The metric included in the default `plugin.json` consists of a `timeseries` section and a `source` section.
Adding an additional metric just requires to add an additional entry to the already existing `metrics` array.

```json
...
    "metrics": [
        {
            "timeseries": {
                "key": "num_files_home_folder",
                "unit": "Count",
                "displayname": "Files"
            },
            "source": {
                "command": "/home/reinhard/listfiles",
                "eval": "(.*)"
            }
        }
    ],
...
```
The `timeseries` section defines the metric for Dynatrace, with `key` assigning it a unique identifier, the `unit` of the metric and a `displayname`.
The `source` section is getting evaluated by the Python code of the plugin, with the `command` specifiying the fully qualified path to the executable to run and `eval` expected to provide a regular expression that extracts a discrete number from the output of the executed command. The property `eval` may be omitted if the executed command already delivers as its output a discrete number. In other words, the eval value `(.*)` in this sample is not necessary.

### Visualization
The metric definition just takes care of collecting data. In order to get the timeseries values visualized properly, also the `ui` section needs to get extended, specifically the `charts` array needs an additional entry.

```json
...
	"ui": {
		"charts": [
            {
                "group": "Home Folder",
                "title": "Number of Files",
                "description": " ",
                "series": [
                    {
                        "key": "num_files_home_folder",
                        "displayname": "Avg Number of Files",
                        "aggregation": "avg",
                        "seriestype": "bar",
                        "stacked": false,
                        "color": "#e31a1c"
                    }
                 ]
            }
        ]
	}
...
```

Visualizing a metric essentially means to define what the chart should look like where it is supposed to appear.
You can add a timeseries either into an existing chart (where it shares the chart with other metrics) or you create an entirely new chart.
The `group` property allows for separating timeseries for different topics into their own tab within the Tenant UI.
Adding a timeseries to a chart requires an additional entry within the `series` array, where the property `key` is the property that refers to the unique identifier defined within the `metric ` section. The properties `displayname`, `aggregation`, `seriestype`, `stacked` and `color` may get omitted and will have default values if not specified.

## Visualization within your Tenant Web UI
The type of entity this plugin is collecting data for are hosts. Therefore you need to navigate to the Details page of the host it is installed on.
A click on the Elipsis as seen on this screenshot reveals the menu entry `Plugin Metrics`.
![Menu](/images/menu.png)
![Chart](/images/chart.png)
