"""
Calculates the total number of unique sites or cells
at the network level.



"""
from typing import List, Optional, Tuple, Union
from ...core.context import get_db
from ...core.mixins import GeoDataMixin
from ...core import location_joined_query, make_spatial_unit
from ...core.spatial_unit import AnySpatialUnit
from ...core.query import Query
from ..utilities import EventsTablesUnion
from flowmachine.utils import standardise_date, Statistic
valid_periods = ['second', 'minute', 'hour', 'day', 'month', 'year']

class TotalNetworkObjects(GeoDataMixin, Query):
    """
    Class for calculating unique cells/sites per location
    and aggregate it by period.

    Parameters
    ----------
    start : datetime
        Start time to filter query.
    stop : datetime
        Stop time to filter query.
    total_by : {'second', 'minute', 'hour', 'day', 'month', 'year'}
        A period definition to group data by.
    table : str
        Either 'calls', 'sms', or other table under `events.*`. If no specific
        table is provided this will collect statistics from all tables.
    network_object : flowmachine.core.spatial_unit.*SpatialUnit, default cell
        Objects to track, defaults to CellSpatialUnit(), the unversioned lowest
        level of infrastructure available.
        Must have network_object.is_network_object == True.
    spatial_unit : flowmachine.core.spatial_unit.*SpatialUnit, default admin0
        Spatial unit to facet on.
        Must have spatial_unit.is_network_object == False.

    Other Parameters
    ----------------
    Passed to EventsTablesUnion

    Examples
    --------
    >>> t = TotalNetworkObjects()
    >>> t.get_dataframe()
       total                  datetime
    0     55 2016-01-01 00:00:00+00:00
    1     55 2016-01-02 00:00:00+00:00
    ...

    """

    def __init__(self, start=None, stop=None, *, table='all', total_by='day', network_object: AnySpatialUnit=make_spatial_unit('cell'), spatial_unit: Optional[AnySpatialUnit]=None, hours: Optional[Tuple[int, int]]=None, subscriber_subset=None, subscriber_identifier='msisdn'):
        self.start = standardise_date(get_db().min_date(table=table) if start is None else start)
        self.stop = standardise_date(get_db().max_date(table=table) if stop is None else stop)
        self.table = table
        if isinstance(self.table, str):
            self.table = self.table.lower()
            if self.table != 'all' and (not self.table.startswith('events')):
                self.table = 'events.{}'.format(self.table)
        network_object.verify_criterion('is_network_object')
        self.network_object = network_object
        if spatial_unit is None:
            self.spatial_unit = make_spatial_unit('admin', level=0)
        else:
            self.spatial_unit = spatial_unit
        self.spatial_unit.verify_criterion('is_network_object', negate=True)
        events = location_joined_query(EventsTablesUnion(self.start, self.stop, tables=self.table, columns=['location_id', 'datetime'], hours=hours, subscriber_subset=subscriber_subset, subscriber_identifier=subscriber_identifier), spatial_unit=self.network_object, time_col='datetime')
        self.joined = location_joined_query(events, spatial_unit=self.spatial_unit, time_col='datetime')
        self.total_by = total_by.lower()
        if self.total_by not in valid_periods:
            raise ValueError('{} is not a valid total_by value.'.format(self.total_by))
        super().__init__()

    @property
    def column_names(self) -> List[str]:
        return self.spatial_unit.location_id_columns + ['value', 'datetime']

    def _make_query(self):
        cols = self.network_object.location_id_columns
        group_cols = self.spatial_unit.location_id_columns
        for column in group_cols:
            if column in cols:
                cols.remove(column)
        cols_str = ','.join(cols)
        group_cols_str = ','.join(group_cols)
        sql = f"\n        SELECT {group_cols_str}, COUNT(*) as value,\n             datetime FROM\n              (SELECT DISTINCT {group_cols_str}, {cols_str}, datetime FROM           \n                (SELECT {group_cols_str}, {cols_str}, date_trunc('{self.total_by}', x.datetime) AS datetime\n                FROM ({self.joined.get_query()}) x) y) _\n            GROUP BY {group_cols_str}, datetime\n            ORDER BY {group_cols_str}, datetime\n        "
        return sql

class AggregateNetworkObjects(GeoDataMixin, Query):
    """
    Class for calculating statistics about unique cells/sites
    and aggregate it by period.

    Parameters
    ----------
    total_network_objects : TotalNetworkObjects

    statistic : Statistic
        Statistic to calculate, defaults to Statistic.AVG

    aggregate_by : {'second', 'minute', 'hour', 'day', 'month', 'year', 'century'}
        A period definition to calculate statistics over, defaults to the one
        greater than total_network_objects.total_by.

    Examples
    --------
    >>> t = AggregateNetworkObjects(total_network_objects=TotalNetworkObjects())
    >>> t.get_dataframe()
          name  total                  datetime
    0  Nepal     55 2016-01-01 00:00:00+00:00
    1  Nepal     55 2016-01-02 00:00:00+00:00
    2  Nepal     55 2016-01-03 00:00:00+00:00
    3  Nepal     55 2016-01-04 00:00:00+00:00
    4  Nepal     55 2016-01-05 00:00:00+00:00
    ...

    """

    def __init__(self, *, total_network_objects, statistic: Union[Statistic, str]=Statistic.AVG, aggregate_by=None):
        self.total_objs = total_network_objects
        self.statistic = Statistic(statistic.lower())
        if aggregate_by is None:
            if self.total_objs.total_by == 'second':
                self.aggregate_by = 'minute'
            elif self.total_objs.total_by == 'minute':
                self.aggregate_by = 'hour'
            elif self.total_objs.total_by == 'hour':
                self.aggregate_by = 'day'
            elif self.total_objs.total_by == 'day':
                self.aggregate_by = 'month'
            elif self.total_objs.total_by == 'month':
                self.aggregate_by = 'year'
            else:
                self.aggregate_by = 'century'
        else:
            self.aggregate_by = aggregate_by
        if self.aggregate_by not in valid_periods + ['century']:
            raise ValueError('{} is not a valid aggregate_by value.'.format(self.aggregate_by))
        self.spatial_unit = self.total_objs.spatial_unit
        super().__init__()

    @property
    def column_names(self) -> List[str]:
        return self.spatial_unit.location_id_columns + ['value', 'datetime']

    def _make_query(self):
        group_cols = ','.join(self.spatial_unit.location_id_columns)
        sql = f"\n        SELECT {group_cols}, {self.statistic:z.value} as value,\n        date_trunc('{self.aggregate_by}', z.datetime) as datetime FROM \n            ({self.total_objs.get_query()}) z\n        GROUP BY {group_cols}, date_trunc('{self.aggregate_by}', z.datetime)\n        ORDER BY {group_cols}, date_trunc('{self.aggregate_by}', z.datetime)\n        "
        return sql