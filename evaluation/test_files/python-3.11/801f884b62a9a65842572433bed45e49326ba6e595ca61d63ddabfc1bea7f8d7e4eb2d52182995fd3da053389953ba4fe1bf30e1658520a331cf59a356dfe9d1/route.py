"""
Route command module.
"""
__author__ = 'Julia Patacz'
__copyright__ = 'Copyright (C) 2018, Nokia'
__email__ = 'julia.patacz@nokia.com'
import re
from moler.cmd.unix.genericunix import GenericUnixCommand
from moler.exceptions import CommandFailure
from moler.exceptions import ParsingDone

class Route(GenericUnixCommand):

    def __init__(self, connection, prompt=None, newline_chars=None, options=None, runner=None):
        super(Route, self).__init__(connection=connection, prompt=prompt, newline_chars=newline_chars, runner=runner)
        self.options = options
        self.headers = []
        self.values = []
        self.ret_required = False

    def build_command_string(self):
        cmd = 'route'
        if self.options:
            cmd = '{} {}'.format(cmd, self.options)
        return cmd

    def on_new_line(self, line, is_full_line):
        if is_full_line:
            try:
                self._parse_values(line)
                self._parse_header(line)
                self._parse_fail(line)
            except ParsingDone:
                pass
        return super(Route, self).on_new_line(line, is_full_line)
    _re_headers = re.compile('(?P<head_1>\\S+)\\s+(?P<head_2>\\S+)\\s+(?P<head_3>\\S+)\\s+(?P<head_4>\\S+)\\s+(?P<head_5>\\S+)\\s+(?P<head_6>\\S+)\\s+(?P<head_7>\\S+)\\s+(?P<head_8>\\S+)')

    def _parse_header(self, line):
        if self._regex_helper.search_compiled(Route._re_headers, line):
            self.headers = []
            self.headers.append(self._regex_helper.group('head_1'))
            self.headers.append(self._regex_helper.group('head_2'))
            self.headers.append(self._regex_helper.group('head_3'))
            self.headers.append(self._regex_helper.group('head_4'))
            self.headers.append(self._regex_helper.group('head_5'))
            self.headers.append(self._regex_helper.group('head_6'))
            self.headers.append(self._regex_helper.group('head_7'))
            self.headers.append(self._regex_helper.group('head_8'))
            self.current_ret['headers'] = self.headers
            raise ParsingDone
    _re_values = re.compile('(?P<val_1>\\S+)\\s+(?P<val_2>\\S+)\\s+(?P<val_3>\\S+)\\s+(?P<val_4>\\S+)\\s+(?P<val_5>\\S+)\\s+(?P<val_6>\\S+)\\s+(?P<val_7>\\S+)\\s+(?P<val_8>\\S+)')

    def _parse_values(self, line):
        if self.headers and self._regex_helper.search_compiled(Route._re_values, line):
            self.values.append(self._regex_helper.group('val_1'))
            self.values.append(self._regex_helper.group('val_2'))
            self.values.append(self._regex_helper.group('val_3'))
            self.values.append(self._regex_helper.group('val_4'))
            self.values.append(self._regex_helper.group('val_5'))
            self.values.append(self._regex_helper.group('val_6'))
            self.values.append(self._regex_helper.group('val_7'))
            self.values.append(self._regex_helper.group('val_8'))
            key = '{}_{}'.format(self._regex_helper.group('val_8'), self._regex_helper.group('val_1'))
            if key not in self.current_ret.keys():
                self.current_ret[key] = {}
            for i in range(0, len(self.headers)):
                self.current_ret[key][self.headers[i]] = self.values[i]
            self.values = []
            raise ParsingDone
    _re_fail = re.compile('.*:\\s+File exists|.*:\\s+No such device|.*:\\s+No such process')

    def _parse_fail(self, line):
        if self._regex_helper.search_compiled(Route._re_fail, line):
            self.set_exception(CommandFailure(self, "Command failed in line '{}'".format(line)))
            raise ParsingDone
COMMAND_OUTPUT = '\nroot@debdev:/home/ute/moler# route\nKernel IP routing table\nDestination     Gateway         Genmask         Flags Metric Ref    Use Iface\ndefault         10.0.2.2        0.0.0.0         UG    1024   0        0 eth0\n10.0.2.0        *               255.255.255.0   U     0      0        0 eth0\nlink-local      *               255.255.0.0     U     1000   0        0 eth0\nroot@debdev:/home/ute/moler#\n'
COMMAND_KWARGS = {}
COMMAND_RESULT = {'eth0_10.0.2.0': {'Destination': '10.0.2.0', 'Flags': 'U', 'Gateway': '*', 'Genmask': '255.255.255.0', 'Iface': 'eth0', 'Metric': '0', 'Ref': '0', 'Use': '0'}, 'eth0_default': {'Destination': 'default', 'Flags': 'UG', 'Gateway': '10.0.2.2', 'Genmask': '0.0.0.0', 'Iface': 'eth0', 'Metric': '1024', 'Ref': '0', 'Use': '0'}, 'eth0_link-local': {'Destination': 'link-local', 'Flags': 'U', 'Gateway': '*', 'Genmask': '255.255.0.0', 'Iface': 'eth0', 'Metric': '1000', 'Ref': '0', 'Use': '0'}, 'headers': ['Destination', 'Gateway', 'Genmask', 'Flags', 'Metric', 'Ref', 'Use', 'Iface']}
COMMAND_OUTPUT_extended = '\nroot@debdev:/home/ute# route -e\nKernel IP routing table\nDestination     Gateway         Genmask         Flags   MSS Window  irtt Iface\ndefault         10.0.2.2        0.0.0.0         UG        0 0          0 eth0\n10.0.2.0        *               255.255.255.0   U         0 0          0 eth0\nlink-local      *               255.255.0.0     U         0 0          0 eth0\nroot@debdev:/home/ute# '
COMMAND_KWARGS_extended = {'options': '-e'}
COMMAND_RESULT_extended = {'eth0_10.0.2.0': {'Destination': '10.0.2.0', 'Flags': 'U', 'Gateway': '*', 'Genmask': '255.255.255.0', 'Iface': 'eth0', 'MSS': '0', 'Window': '0', 'irtt': '0'}, 'eth0_default': {'Destination': 'default', 'Flags': 'UG', 'Gateway': '10.0.2.2', 'Genmask': '0.0.0.0', 'Iface': 'eth0', 'MSS': '0', 'Window': '0', 'irtt': '0'}, 'eth0_link-local': {'Destination': 'link-local', 'Flags': 'U', 'Gateway': '*', 'Genmask': '255.255.0.0', 'Iface': 'eth0', 'MSS': '0', 'Window': '0', 'irtt': '0'}, 'headers': ['Destination', 'Gateway', 'Genmask', 'Flags', 'MSS', 'Window', 'irtt', 'Iface']}
COMMAND_OUTPUT_cached = '\nroot@debdev:/home/ute# route -C\nKernel IP routing cache\nSource          Destination     Gateway         Flags Metric Ref    Use Iface\nroot@debdev:/home/ute# '
COMMAND_KWARGS_cached = {'options': '-C'}
COMMAND_RESULT_cached = {'headers': ['Source', 'Destination', 'Gateway', 'Flags', 'Metric', 'Ref', 'Use', 'Iface']}
COMMAND_OUTPUT_add = '\nroot@debdev:/home/ute# route add -net 0.0.0.0 netmask 0.0.0.0 gw 10.0.2.2\nroot@debdev:/home/ute# '
COMMAND_KWARGS_add = {'options': 'add -net 0.0.0.0 netmask 0.0.0.0 gw 10.0.2.2'}
COMMAND_RESULT_add = {}