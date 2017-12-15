# oneagent-generic-execution-plugin
A Sample OneAgent Plugin that collects additional metrics for the host it is deployed on by executing configurable commands

## Motivation for this project
The entities (hosts, processes, ...) in your environment, that are monitored by Dynatrace, ususally offer many more metrics than the Dynatrace OneAgent is collecting out of the box.

Specifically for host metrics it's very often just a matter of invoking an already existing utility on the command line that provides these metrics.

This Plugin allows you to specify configure these additional metrics within the ```plugin.json``` file alongside with the command line to invoke and a regular expression that extracts the timeseries data from the output delivered by this command.

## Installation
