import subprocess
from ruxit.api.base_plugin import BasePlugin
from ruxit.api.snapshot import pgi_name
from ruxit.api.selectors import HostSelector
import logging
import re

class GenExecPlugin(BasePlugin):

        def initialize(self, **kwargs):
                self.json_config = kwargs["json_config"]
                self.metrics = kwargs["json_config"]["metrics"]

        def query(self, **kwargs):
                logger = logging.getLogger('GenExecPlugin')
                config = kwargs["config"]

                host_id =  self.query_snapshot.host_id;

                for metric in self.metrics:
                        timeseries = None
                        metric_key = None

                        try:
                                timeseries = metric["timeseries"]
                        except KeyError:
                                continue

                        try:
                                metric_key = timeseries["key"]
                        except KeyError:
                                continue

                        reg = "(.*)"
                        cmds = None
                        cmd = None
                        source = None
                        try:
                                source  =  metric["source"]
                        except KeyError:
                                logger.warning("The metric %s does not contain a source attribute", metric_key)
                                continue

                        try:
                                cmd  =  source["command"]
                        except KeyError:
                                logger.warning("The source attribute of metric %s does not contain a command attribute", metric_key)
                                continue

                        cmds  =  cmd.split(" ")

                        try:
                                reg  =  source["eval"]
                        except KeyError:
                                pass

                        p = None
                        try:
                                p = subprocess.Popen(cmds, shell = True,  stdin = subprocess.PIPE,  stdout = subprocess.PIPE,  stderr =subprocess.PIPE)
                        except:
                                logger.error("unable to invoke %s for metric %s", cmd, metric_key, exc_info = True)
                                continue

                        stdout_lines = p.stdout.readlines(-1)

                        if (len(stdout_lines) <= 0):
                            stderr_lines = p.stderr.readlines(-1)
                            if (len(stderr_lines) > 0):
                                for i in range(len(stderr_lines)):
                                    logger.warning(stderr_lines[i])
                            return
                        text = stdout_lines[0]
                        text = text.decode('utf8')

                        extracted = None
                        try:
                                extracted = re.search(reg, text).group(0)
                        except:
                                logger.error("failed to apply regular expression %s on output %s for metric %s", reg, text, metric_key, exc_info = True)
                                continue

                        stat_value = None
                        try:
                                stat_value = float(extracted)
                        except:
                                logger.error("the value %s extracted from the output when executing %s for the metric %s is not a number", extracted, cmd, metric_key, exc_info = True)
                                continue

                        try:
                                self.results_builder.absolute(
                                        key = metric_key,
                                        value = stat_value,
                                        entity_id = host_id
                                )
                        except:
                                pass
