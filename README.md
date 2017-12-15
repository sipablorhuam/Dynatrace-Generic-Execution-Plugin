# oneagent-generic-execution-plugin
A Sample OneAgent Plugin that collects additional metrics for the host it is deployed on by executing configurable commands

## Motivation for this project
The entities (hosts, processes, ...) in your environment, that are monitored by Dynatrace, ususally offer many more metrics than the Dynatrace OneAgent is collecting out of the box.

Specifically for host metrics it's very often just a matter of invoking an already existing utility on the command line that provides these metrics.

This Plugin allows you to specify configure these additional metrics within the `plugin.json` file alongside with the command line to invoke and a regular expression that extracts the timeseries data from the output delivered by this command.
There is however no need to modify the Python Code of the Plugin, unless you would like to extend it with additional functionality.

## Installation
OneAgent Plugins need to get installed both, on you Tenant and on the host(s) they are supposed to collect data for - mainly for security reasons. NO third party code is getting executed by your OneAgent unless your Tenant and your Agent agree on the authenticity of your plugin.
This is why you need to install, in addition to your Tenant, on selected Hosts, that have OneAgent running and are supposed to execute your Plugin.
### Installation on your Dynatrace Tenant
* Package the file `plugin.json` and `gen_exec_plugin.py` into a zip archive named `custom.python.generic_exec_plugin.zip`.
* Navigate in the Web Interface of your Tenant to `Settings / Monitoring / Monitored Technologies` and select the tab `Custom Plugins`.
* Click on the button `Upload Plugin` and install your zip archive on your tenant.
* Select the new entry in the list of your plugins and promote it from Staging to Production
### Installation on your monitored host
* Create a folder name `custom.python.generic_exec_plugin` within `/opt/dynatrace/oneagent/plugin_deployment`
* Copy `plugin.json` and `gen_exec_plugin.py` into that folder
* Restart Oneagent (e.g. `sudo service oneagent restart`)

## Customization
This Project by default just invokes a sample executable it expects to find on your monitored host.
In order to add more metrics to be captured you will need to modify the `plugin.json` before deploying the Plugin.

```json
    "metrics": [
        {
            "timeseries": {
                "key": "num_files_home_folder",
                "unit": "Count",
                "displayname": "Files"
            },
            "source": {
                "command": "/home/reinhard/listfiles"
            }
        }
    ],
```
