"""
The population-weighted opportunities model uses
population distributions for predicting the
probability of movement between populated
areas. The model computes the attraction
between populated centers relative to the
distance between each origin and destination
locations and also to all other equidistant
locations from the destination. The model
works similarly to the Radiation Model.

The original publication suggests that its
ideal usage is in cities.



References
----------
    Yan X-Y, Zhao C, Fan Y, Di Z, Wang W-X. 2014 "Universal predictability of mobility patterns in cities". J. R. Soc. Interface 11: 20140834. http://dx.doi.org/10.1098/rsif.2014.0834

"""
import warnings
from typing import List, Optional, Union, Tuple
import pandas as pd
from flowmachine.core.query import Query
from flowmachine.features.subscriber import daily_location
from flowmachine.utils import list_of_dates, standardise_date
from flowmachine.features.subscriber import ModalLocation
from flowmachine.core import make_spatial_unit
from flowmachine.core.spatial_unit import LonLatSpatialUnit
from flowmachine.features.spatial.distance_matrix import DistanceMatrix
import structlog
logger = structlog.get_logger('flowmachine.debug', submodule=__name__)

class _PopulationBuffer(Query):
    """
    Private class for calculating a population
    vector based on buffers generated from
    the distance radii between point locations.

    Parameters
    ----------
    population_object : flowmachine.features.utilities.spatial_aggregate.SpatialAggregate
        An aggregated subscriber locating object
    distance_matrix : flowmachine.features.spatial.distance_matrix.DistanceMatrix
        A distance matrix
    """

    def __init__(self, population_object, distance_matrix):
        self.population_object = population_object
        self.distance_matrix = distance_matrix
        self.spatial_unit = self.distance_matrix.spatial_unit
        super().__init__()

    @property
    def column_names(self) -> List[str]:
        cols = self.spatial_unit.location_id_columns
        return [f'{c}_from' for c in cols] + [f'{c}_to' for c in cols] + ['buffer_population', 'src_pop', 'sink_pop']

    def _make_query(self):
        """
        Protected method that generates SQL
        that calculates the population that is
        covered by a buffer.
        """
        cols = self.spatial_unit.location_id_columns
        sql = f"\n        SELECT   \n        {', '.join((f'{c}_{direction}' for direction in ('from', 'to') for c in cols))},\n         1/(sum(src_pop) over (partition by {', '.join((f'{c}_to' for c in cols))} order by value)+sink_pop-src_pop) as buffer_population,\n         src_pop, sink_pop \n         FROM (\n            (SELECT * FROM \n            (SELECT {', '.join((f'hl_{direction}.{c} as {c}_{direction}' for c in cols for direction in ('to', 'from')))}, hl_from.value as src_pop, hl_to.value as sink_pop\n            FROM\n            ({self.population_object.get_query()}) as hl_from\n            LEFT JOIN \n            ({self.population_object.get_query()}) as hl_to\n            ON \n                {' OR '.join((f'hl_from.{c} != hl_to.{c}' for c in cols))}\n            ) pops\n            LEFT JOIN\n            ({self.distance_matrix.get_query()}) as dm\n            USING ({', '.join((f'{c}_{direction}' for c in cols for direction in ('to', 'from')))})\n            )\n         ) distance_pop_matrix\n        \n        "
        return sql

class PopulationWeightedOpportunities(Query):
    """
    Population-weighted opportunities model [1]_.
    The model predicts the mobility between populated
    areas in cities based only on the population densities
    of those areas, their spatial distribution, and
    the number of people that depart a certain area. This
    model is useful for studying mobility pattern in cities.

    Parameters
    ----------
    start : str
        ISO format date string denoting the first day of data to include
    stop : str
        ISO format date string denoting the last day of data to include
    spatial_unit : flowmachine.core.spatial_unit.*SpatialUnit, default versioned-site
        Spatial unit to which subscriber locations will be mapped. See the
        docstring of make_spatial_unit for more information.
    departure_rate : float, or Dataframe, default 0.1
        Either one uniform departure rate, or a dataframe with a rate column
        and columns matching those of the spatial unit. If the latter, results
        are only returned for locations in this dataframe
    hours : 'all', or tuple of ints, default 'all'
        The hours of the day to include activity in
    method : {'last', 'most-common'}, default 'last'
        Method used to resolve a daily location
    table : str, or list of str, default 'all'
        Specify which event types to include. 'all', all available event
        types are included. Otherwise, should be a (schema qualified) list of
        events tables.
    subscriber_identifier : {'msisdn', 'imei'}, default 'msisdn'
        Either msisdn, or imei, the column that identifies the subscriber.
    subscriber_subset : flowmachine.core.Query, default None
        If provided, a query or table which has a column with a named
        subscriber to limit results to.

    Examples
    --------
    >>> p = PopulationWeightedOpportunities('2016-01-01', '2016-01-07', departure_rate=pd.Dataframe([{"site_id":'0xqNDj', "rate":0.9}]))

    One can also run the model with uniform departure
    rates for all locations as follows:

    >>> PopulationWeightedOpportunities('2016-01-01', '2016-01-07', departure_rate=0.5).head()
        origin  destination  prediction  probability
    0  0xqNDj        8wPojr    0.384117     0.010670
    1  0xqNDj        B8OaG5    0.344384     0.009566
    2  0xqNDj        DonxkP    0.715311     0.019870
    3  0xqNDj        zdNQx2    0.267854     0.007440

    Where prediction is the absolute number of people
    that move from one location to another. (This should
    be interpreted as a integer, but floats are provided
    for evaluating results in a continuous scale.) And
    probability is the predicted value over the total
    population leaving the origin (T_i). That is, how
    likely it is that a person leaving the origin will
    be found in a given destination.

    References
    ----------
    .. [1] Yan X-Y, Zhao C, Fan Y, Di Z, Wang W-X. 2014 "Universal predictability of mobility patterns in cities". J. R. Soc. Interface 11: 20140834. http://dx.doi.org/10.1098/rsif.2014.0834
    """

    def __init__(self, start: str, stop: str, *, spatial_unit: Optional[LonLatSpatialUnit]=None, departure_rate: Union[pd.DataFrame, float]=0.1, hours: Union[str, Tuple[int, int]]='all', method: str='last', table: Union[str, List[str]]='all', subscriber_identifier: str='msisdn', subscriber_subset: Optional[Query]=None):
        warnings.warn('The PopulationWeightedOpportunities model is currently **experimental**. ' + 'Please review Yan X-Y et al. ' + '(http://dx.doi.org/10.1098/rsif.2014.0834) ' + 'before using this model in production.')
        if isinstance(departure_rate, pd.DataFrame):
            self.departure_rate = departure_rate.rename(columns=lambda x: x if x == 'rate' else f'{x}_from').apply(lambda x: x.sort_values().values)
            self.departure_rate = self.departure_rate.reindex(columns=sorted(self.departure_rate.columns))
        elif isinstance(departure_rate, float):
            self.departure_rate = departure_rate
        else:
            raise TypeError(f'{departure_rate} must be a float or dataframe')
        self.start = standardise_date(start)
        self.stop = standardise_date(stop)
        if spatial_unit is None:
            self.spatial_unit = make_spatial_unit('versioned-site')
        else:
            self.spatial_unit = spatial_unit
        self.distance_matrix = DistanceMatrix(spatial_unit=self.spatial_unit, return_geometry=True)
        self.population_object = ModalLocation(*[daily_location(d, spatial_unit=self.spatial_unit, hours=hours, method=method, table=table, subscriber_identifier=subscriber_identifier, ignore_nulls=True, subscriber_subset=subscriber_subset) for d in list_of_dates(self.start, self.stop)]).aggregate()
        self.population_buffer_object = _PopulationBuffer(population_object=self.population_object, distance_matrix=self.distance_matrix)

    @property
    def column_names(self) -> List[str]:
        return ['{}_{}'.format(c, d) for d in ('from', 'to') for c in self.spatial_unit.location_id_columns] + ['prediction', 'probability']

    def _make_query(self):
        if isinstance(self.departure_rate, float):
            scaled_buffer_query = f'SELECT buffer.src_pop*{self.departure_rate} as T_i, * FROM buffer'
        elif isinstance(self.departure_rate, pd.DataFrame):
            scaled_buffer_query = f"\n            SELECT buffer.*, buffer.src_pop*rate as T_i FROM \n            (VALUES {', '.join([str(tuple(x)) for x in self.departure_rate.values])}) \n                AS t({', '.join((c for c in self.departure_rate.columns))})\n                LEFT JOIN buffer\n                USING ({', '.join((c for c in self.departure_rate.columns if c != 'rate'))})\n            "
        else:
            raise ValueError(f'Unexpected departure rate type! Got {self.departure_rate}.')
        return f"\n        WITH buffer AS ({self.population_buffer_object.get_query()}),\n        beta AS (SELECT 1.0/sum(value) as beta FROM ({self.population_object.get_query()}) pops),\n        sigma AS (\n            SELECT\n             {', '.join((f'{c}_from' for c in self.spatial_unit.location_id_columns))},\n             sum(sink_pop*(buffer_population-(SELECT beta FROM beta))) as sigma\n             FROM buffer\n             GROUP BY {', '.join((f'{c}_from' for c in self.spatial_unit.location_id_columns))}\n        )\n        SELECT {', '.join(('{}_{}'.format(c, d) for d in ('from', 'to') for c in self.spatial_unit.location_id_columns))}, prediction, COALESCE(prediction / T_i, 0.) as probability\n        FROM\n        (SELECT {', '.join(('{}_{}'.format(c, d) for d in ('from', 'to') for c in self.spatial_unit.location_id_columns))},\n            NULLIF(T_i, 0) as T_i,\n            (T_i*sink_pop*(buffer_population-(SELECT beta FROM beta)))/sigma as prediction\n        \n        FROM\n        ({scaled_buffer_query}) scaled_buf\n        LEFT JOIN\n        sigma\n        USING ({', '.join((f'{c}_from' for c in self.spatial_unit.location_id_columns))}) ) pwo_pred\n            \n        "