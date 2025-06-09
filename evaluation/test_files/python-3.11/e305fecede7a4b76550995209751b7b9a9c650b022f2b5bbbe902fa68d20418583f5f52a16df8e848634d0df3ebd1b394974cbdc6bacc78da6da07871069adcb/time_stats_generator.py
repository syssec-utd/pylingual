"""Module that computes statistics for features of Time type.

This module determines whether values are in the Time semantic domain in
different ways, depending on the data type of the values. If the values are
strings, it uses defined lists of date formats and time formats written
with strptime directives along with delimiters (for building date and time
combinations) to create a list of regexes against which each value is matched.
If the values are integers, it uses ranges of values that correspond to valid
Unix times. This generator considers times that fall on or after
01-Jan-90 00:00:00 UTC and before 01-Jan-30 00:00:00 UTC to be valid times when
analyzing integers.

The TimeStatsGenerator tracks the most common matching time format across all
input values. If the match rate for that format is high enough (as compared to
the match_ratio) and enough values have been considered (as compared to the
values_threshold), then the feature is marked as Time by generating the
appropriate domain_info with format as a custom statsistic.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import calendar
import collections
import re
import numpy as np
import pyarrow as pa
from tensorflow_data_validation import types
from tensorflow_data_validation.arrow import arrow_util
from tensorflow_data_validation.statistics.generators import stats_generator
from tensorflow_data_validation.utils import stats_util
from typing import Iterable, Pattern, Text, Tuple
from tensorflow_metadata.proto.v0 import schema_pb2
from tensorflow_metadata.proto.v0 import statistics_pb2
_MATCH_RATIO = 0.8
_VALUES_THRESHOLD = 100
_UnixTime = collections.namedtuple('_UnixTime', ['format_constant', 'begin', 'end'])
_UNIX_TIMES = [_UnixTime(format_constant=schema_pb2.TimeDomain.UNIX_SECONDS, begin=631152000, end=1893456000), _UnixTime(format_constant=schema_pb2.TimeDomain.UNIX_MILLISECONDS, begin=631152000000, end=1893456000000), _UnixTime(format_constant=schema_pb2.TimeDomain.UNIX_MICROSECONDS, begin=631152000000000, end=1893456000000000), _UnixTime(format_constant=schema_pb2.TimeDomain.UNIX_NANOSECONDS, begin=631152000000000000, end=1893456000000000000)]
_UNIX_TIME_FORMATS = set([time.format_constant for time in _UNIX_TIMES])
_MATCHING_FORMAT = 'time_format'
_TIME_MATCH_RATIO = 'time_match_ratio'
_STRPTIME_TO_RE = {'%B': '(?:' + '|'.join(calendar.month_name[1:]) + ')', '%f': '(?:[0-9]{1,6})', '%d': '(?:3[0-1]|[1-2]\\d|0[1-9]|[1-9]| [1-9])', '%H': '(?:2[0-3]|[0-1]\\d|\\d)', '%y': '(?:\\d\\d)', '%Y': '(?:\\d\\d\\d\\d)', '%m': '(?:1[0-2]|0[1-9]|[1-9])', '%M': '(?:[0-5]\\d|\\d)', '%S': '(?:60[0-1]|[0-5]\\d|\\d)'}
_TIME_DELIMITERS = ['T', ' ']
_DATE_ONLY_FORMATS = ['%Y-%m-%d', '%Y/%m/%d', '%Y%m%d', '%y-%m-%d', '%y/%m/%d', '%m-%d-%Y', '%m/%d/%Y', '%m%d%Y', '%m-%d-%y', '%m/%d/%y', '%d-%m-%Y', '%d/%m/%Y', '%d%m%Y', '%d-%B-%Y', '%d-%m-%y', '%d/%m/%y', '%d-%B-%y']
_TIME_ONLY_FORMATS = ['%H:%M', '%H:%M:%S', '%H:%M:%S.%f']

def _convert_strptime_to_regex(strptime_str: Text) -> Text:
    """Converts a string that includes strptime directives to a regex.

  Args:
    strptime_str: A string that includes strptime directives.

  Returns:
    A string that copies strptime_str but has the any directives in
      _STRPTIME_TO_RE replaced with their corresponding regexes.
  """

    def _get_replacement_regex(matchobj):
        return _STRPTIME_TO_RE[matchobj.group(0)]
    all_directives_re = re.compile('|'.join(_STRPTIME_TO_RE))
    return re.sub(all_directives_re, _get_replacement_regex, strptime_str)

def _build_all_formats() -> Iterable[Text]:
    """Yields all valid date, time, and combination formats.

  The valid formats are defined by _DATE_ONLY_FORMATS, _TIME_ONLY_FORMATS, and
  _TIME_DELIMITERS. This function yields each date only and time only format.
  For combination formats, each date format from _DATE_ONLY_FORMATS is combined
  with each time format from _TIME_ONLY_FORMATS in two ways: one with the time
  delimiter and one with a space.

  Yields:
    All valid date, time, and combination date and time formats.
  """
    for date_fmt in _DATE_ONLY_FORMATS:
        yield date_fmt
    for time_fmt in _TIME_ONLY_FORMATS:
        yield time_fmt
    for date_fmt in _DATE_ONLY_FORMATS:
        for time_fmt in _TIME_ONLY_FORMATS:
            for time_delimiter in _TIME_DELIMITERS:
                yield ''.join([date_fmt, time_delimiter, time_fmt])

def _build_all_formats_regexes(strptime_formats: Iterable[Text]) -> Iterable[Tuple[Text, Pattern[Text]]]:
    """Yields compiled regexes corresponding to the input formats.

  Args:
    strptime_formats: Strptime format strings to convert to regexes.

  Yields:
    (strptime_format, compiled regex) tuples.
  """
    for strptime_format in strptime_formats:
        compiled_regex = re.compile('^{}$'.format(_convert_strptime_to_regex(strptime_format)))
        yield (strptime_format, compiled_regex)
_TIME_RE_LIST = list(_build_all_formats_regexes(_build_all_formats()))

class _PartialTimeStats(object):
    """Partial feature stats for dates/times."""

    def __init__(self, considered: int=0, invalidated: bool=False) -> None:
        self.considered = considered
        self.invalidated = invalidated
        self.matching_formats = collections.Counter()

    def __add__(self, other: '_PartialTimeStats') -> '_PartialTimeStats':
        """Merges two partial stats."""
        self.considered += other.considered
        self.invalidated |= other.invalidated
        self.matching_formats.update(other.matching_formats)
        return self

    def update(self, values: np.ndarray, value_type: types.FeatureNameStatisticsType) -> None:
        """Updates the partial Time statistics using the values.

    Args:
      values: A numpy array of values in a batch.
      value_type: The type of the values.
    """
        self.considered += values.size
        if value_type == statistics_pb2.FeatureNameStatistics.STRING:
            for value in values:
                for strptime_format, time_regex in _TIME_RE_LIST:
                    if time_regex.match(value):
                        self.matching_formats[strptime_format] += 1
        elif value_type == statistics_pb2.FeatureNameStatistics.INT:
            for unix_time in _UNIX_TIMES:
                num_matching_values = np.sum((values >= unix_time.begin) & (values < unix_time.end))
                if num_matching_values > 0:
                    self.matching_formats[unix_time.format_constant] += num_matching_values
        else:
            raise ValueError('Attempt to update partial time stats with values of an unsupported type.')

class TimeStatsGenerator(stats_generator.CombinerFeatureStatsGenerator):
    """Generates feature-level statistics for features in the Time domain.

  This generates Time domain stats for input examples. After the statistics are
  combined, it classifies the feature as being in the Time domain iff the
  statistics represent enough values (self._values_threshold) and the match
  ratio is high enough (self._match_ratio). The match ratio is determined by
  comparing the most common matching format to the total number of values
  considered.
  """

    def __init__(self, name: Text='TimeStatsGenerator', match_ratio: float=_MATCH_RATIO, values_threshold: int=_VALUES_THRESHOLD) -> None:
        """Initializes a TimeStatsGenerator.

    Args:
      name: The unique name associated with this statistics generator.
      match_ratio: For a feature to be marked as a Time, the classifier
        match ratio must meet or exceed this ratio. This ratio must be in
        (0, 1]. The classifier match ratio is determined by comparing the most
        common valid matching format to the total number of values considered.
      values_threshold: For a feature to be marked as a Time, at least
        this many values must be considered.

    Raises:
      ValueError: If values_threshold <= 0 or match_ratio not in (0, 1].
    """
        super(TimeStatsGenerator, self).__init__(name)
        if values_threshold <= 0:
            raise ValueError('TimeStatsGenerator expects a values_threshold > 0, got %s.' % values_threshold)
        if not 0 < match_ratio <= 1:
            raise ValueError('TimeStatsGenerator expects a match_ratio in (0, 1].')
        self._match_ratio = match_ratio
        self._values_threshold = values_threshold

    def create_accumulator(self) -> _PartialTimeStats:
        """Returns a fresh, empty accumulator.

    Returns:
      An empty accumulator.
    """
        return _PartialTimeStats()

    def add_input(self, accumulator: _PartialTimeStats, feature_path: types.FeaturePath, feature_array: pa.Array) -> _PartialTimeStats:
        """Returns result of folding a batch of inputs into the current accumulator.

    Args:
      accumulator: The current accumulator.
      feature_path: The path of the feature.
      feature_array: An arrow Array representing a batch of feature values
        which should be added to the accumulator.

    Returns:
      The accumulator after updating the statistics for the batch of inputs.
    """
        if accumulator.invalidated:
            return accumulator
        feature_type = stats_util.get_feature_type_from_arrow_type(feature_path, feature_array.type)
        if feature_type is None:
            return accumulator
        if feature_type == statistics_pb2.FeatureNameStatistics.STRING:

            def _maybe_get_utf8(val):
                return stats_util.maybe_get_utf8(val) if isinstance(val, bytes) else val
            values = np.asarray(arrow_util.flatten_nested(feature_array)[0])
            maybe_utf8 = np.vectorize(_maybe_get_utf8, otypes=[object])(values)
            if not maybe_utf8.all():
                accumulator.invalidated = True
                return accumulator
            accumulator.update(maybe_utf8, feature_type)
        elif feature_type == statistics_pb2.FeatureNameStatistics.INT:
            values = np.asarray(arrow_util.flatten_nested(feature_array)[0])
            accumulator.update(values, feature_type)
        else:
            accumulator.invalidated = True
        return accumulator

    def merge_accumulators(self, accumulators: Iterable[_PartialTimeStats]) -> _PartialTimeStats:
        """Merges several accumulators to a single accumulator value.

    Args:
      accumulators: The accumulators to merge.

    Returns:
      The merged accumulator.
    """
        it = iter(accumulators)
        result = next(it)
        for acc in it:
            result += acc
        return result

    def extract_output(self, accumulator: _PartialTimeStats) -> statistics_pb2.FeatureNameStatistics:
        """Returns the result of converting accumulator into the output value.

    This method will add the time_domain custom stat to the proto if the match
    ratio is at least self._match_ratio. The match ratio is determined by
    dividing the number of values that have the most common valid format by the
    total number of values considered. If this method adds the time_domain
    custom stat, it also adds the match ratio and the most common valid format
    to the proto as custom stats.

    Args:
      accumulator: The final accumulator value.

    Returns:
      A proto representing the result of this stats generator.
    """
        result = statistics_pb2.FeatureNameStatistics()
        if accumulator.invalidated or accumulator.considered < self._values_threshold or (not accumulator.matching_formats):
            return result
        most_common_format, most_common_count = accumulator.matching_formats.most_common(1)[0]
        assert most_common_count > 0
        match_ratio = most_common_count / accumulator.considered
        if match_ratio >= self._match_ratio:
            if most_common_format in _UNIX_TIME_FORMATS:
                result.custom_stats.add(name=stats_util.DOMAIN_INFO, str='time_domain {integer_format: %s}' % most_common_format)
            else:
                result.custom_stats.add(name=stats_util.DOMAIN_INFO, str="time_domain {string_format: '%s'}" % most_common_format)
            result.custom_stats.add(name=_TIME_MATCH_RATIO, num=match_ratio)
        return result