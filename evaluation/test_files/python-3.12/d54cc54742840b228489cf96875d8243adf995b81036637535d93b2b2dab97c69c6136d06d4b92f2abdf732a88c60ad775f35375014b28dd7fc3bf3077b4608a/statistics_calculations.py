import numpy as np
import mobspy.simulation_logging.log_scripts as simlog

def time_series_average(species_string, mobspy_ts):
    """
        Badly named function - Average between all RUNS inside a single time-series

        :param species_string: (str) species string to perform the average upon
        :param mobspy_ts: (MobsPy TimeSeries) MobsPy time series object
        :return: average_series (list) a list with the average values from all runs
    """
    list_series = []
    for series in mobspy_ts:
        if species_string in series.keys():
            list_series.append(series)
    for s1 in list_series:
        for s2 in list_series:
            if s1 == s2:
                continue
            for t1, t2 in zip(s1['Time'], s2['Time']):
                if t1 != t2:
                    simlog.error('Time vectors are different')
    average_series = []
    for j in range(len(mobspy_ts.get_max_time_for_species(species_string))):
        add = 0
        size = 0
        for series in list_series:
            try:
                add = add + series[species_string][j]
                size += 1
            except IndexError:
                pass
            except KeyError:
                pass
        average_series.append(add / size)
    return average_series

def standard_deviation(species_string, mobspy_ts, average_series=None):
    """
        Standard deviation between all RUNS inside a single time-series

        :param species_string: (str) Species string
        :param mobspy_ts: (MobsPy TimeSeries) MobsPy time series object
        :param average_series: (list) if the average series is given it is not recalculated
        :return: deviation_series (list) a list with the standard deviation values from all runs
   """
    if average_series is None:
        average_series = time_series_average(species_string, mobspy_ts)
    deviation_series = []
    for j in range(len(mobspy_ts.get_max_time_for_species(species_string))):
        add = 0
        size = 0
        for series in mobspy_ts:
            try:
                add = add + (average_series[j] - series[species_string][j]) ** 2
                size += 1
            except IndexError:
                pass
            except KeyError:
                pass
        deviation_series.append(np.sqrt(add / size))
    return deviation_series

def average_plus_standard_deviation(species_string, mobspy_ts, average_series=None, deviation_series=None):
    """
        Standard deviation between all RUNS inside a single time-series

        :param species_string: (str) Species string
        :param mobspy_ts: (MobsPy TimeSeries) MobsPy time series object
        :param average_series: (list) if the average series is given it is not recalculated
        :param deviation_series: (list) if the deviation is given it is not recalculated

        :return: series_average (list) = average value of the run,  plus (list) = average + deviation,
        minus (list) = average - deviation,
   """
    if average_series is None:
        series_average = time_series_average(species_string, mobspy_ts)
    if deviation_series is None:
        series_deviation = standard_deviation(species_string, mobspy_ts)
    plus = []
    minus = []
    for average, deviation in zip(series_average, series_deviation):
        plus.append(average + deviation)
        minus.append(average - deviation)
    return (series_average, plus, minus)