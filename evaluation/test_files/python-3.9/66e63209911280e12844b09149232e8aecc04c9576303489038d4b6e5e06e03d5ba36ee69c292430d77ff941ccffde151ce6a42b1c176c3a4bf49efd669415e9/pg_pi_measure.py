"""
This module implements PI tag API coming from PostgreSQL.
.. since: 0.2
"""
from datetime import datetime
import pandas as pd
from dateutil import tz
from psycopg2.errors import UniqueViolation
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from edv_dwh_connector.dwh import DatePK, TimePK, DatetimeFromPK
from edv_dwh_connector.dwh import Dwh
from edv_dwh_connector.exceptions import ValueNotFoundError, ValueAlreadyExistsError
from edv_dwh_connector.pi.cached.cached_pi_measure import CachedPIMeasure
from edv_dwh_connector.pi.db.pg_pi_tag import PgPITag
from edv_dwh_connector.pi.pi_measure import PIMeasure, PIMeasures, PIMeasuresDf
from edv_dwh_connector.pi.pi_tag import PITag
from edv_dwh_connector.pi.writer import Writer

class PgPIMeasure(PIMeasure):
    """
    PI measure from PostgreSQL.
    .. since: 0.2
    """

    def __init__(self, tag: PITag, date: datetime, dwh: Dwh) -> None:
        """
        Ctor.
        :param tag: PI tag
        :param date: Datetime
        :param dwh: Data warehouse
        :raises ValueNotFoundError: If not found
        """
        self.__tag = tag
        self.__date = datetime.strptime(date.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3], '%Y-%m-%d %H:%M:%S.%f').astimezone(tz.UTC)
        with dwh.connection() as conn:
            row = conn.execute(text('SELECT value FROM fact_pi_measure WHERE tag_pk = :tag_pk and date_pk = :date_pk and time_pk = :time_pk and millisecond = :millis'), {'tag_pk': self.__tag.uid(), 'date_pk': DatePK(self.__date.date()).value(), 'time_pk': TimePK(self.__date.time()).value(), 'millis': int(self.__date.microsecond / 1000)}).fetchone()
            if row is None:
                raise ValueNotFoundError('PI measure not found')
            self.__value = row['value']

    def tag(self) -> PITag:
        return self.__tag

    def date(self) -> datetime:
        return self.__date

    def value(self) -> float:
        return float(self.__value)

class PgPIMeasures(PIMeasures):
    """
    PI measures from PostgreSQL.
    .. since: 0.2
    """

    def __init__(self, tag: PITag, dwh: Dwh):
        """
        Ctor.
        :param tag: Tag
        :param dwh: Data warehouse
        """
        self.__tag = tag
        self.__dwh = dwh

    def has_at(self, date: datetime) -> bool:
        has = True
        try:
            PgPIMeasure(self.__tag, date, self.__dwh)
        except ValueNotFoundError:
            has = False
        return has

    def last(self) -> PIMeasure:
        with self.__dwh.connection() as conn:
            row = conn.execute(text('SELECT date_pk, time_pk, millisecond FROM fact_pi_measure ORDER BY date_pk DESC, time_pk DESC, millisecond DESC LIMIT 1')).fetchone()
            if row is None:
                raise ValueNotFoundError('Last PI measure not found')
            return PgPIMeasure(self.__tag, DatetimeFromPK(row[0], row[1], row[2]).value(), self.__dwh)

    def items(self, start: datetime, end: datetime) -> list:
        result = []
        with self.__dwh.connection() as conn:
            for row in conn.execute(text("SELECT date_pk, time_pk, millisecond, value FROM fact_pi_measure WHERE CAST(date_pk || '' || time_pk as bigint) BETWEEN :start AND :end and tag_pk = :tag_pk "), {'start': start.strftime('%Y%m%d%H%M%S'), 'end': end.strftime('%Y%m%d%H%M%S'), 'tag_pk': self.__tag.uid()}).fetchall():
                result.append(PgPIMeasure(self.__tag, DatetimeFromPK(row[0], row[1], row[2]).value(), self.__dwh))
            for row in conn.execute(text("SELECT date_pk, time_pk, millisecond, value FROM fact_pi_measure_hist WHERE CAST(date_pk || '' || time_pk as bigint) BETWEEN :start AND :end and tag_pk = :tag_pk "), {'start': start.strftime('%Y%m%d%H%M%S'), 'end': end.strftime('%Y%m%d%H%M%S'), 'tag_pk': self.__tag.uid()}).fetchall():
                result.append(PgPIMeasure(self.__tag, DatetimeFromPK(row[0], row[1], row[2]).value(), self.__dwh))
        return result

    def add(self, date: datetime, value: float) -> PIMeasure:
        try:
            with self.__dwh.connection() as conn:
                conn.execute(text('INSERT INTO fact_pi_measure (tag_pk, date_pk, time_pk, value, millisecond) VALUES(:tag_pk, :date_pk, :time_pk, :value, :millis) '), {'tag_pk': self.__tag.uid(), 'date_pk': DatePK(date.date()).value(), 'time_pk': TimePK(date.time()).value(), 'value': value, 'millis': int(date.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3].split('.')[1])})
                return PgPIMeasure(self.__tag, date, self.__dwh)
        except IntegrityError as exe:
            assert isinstance(exe.orig, UniqueViolation)
            raise ValueAlreadyExistsError(f'A measure already exists at {date} for tag {self.__tag.code()}') from exe

class PgCachedPIMeasures(PIMeasures):
    """
    Cached PI measures from PostgreSQL.
    .. since: 0.4
    """

    def __init__(self, tag, dwh: Dwh):
        """
        Ctor.
        :param tag: Tag or code of tag
        :param dwh: Data warehouse
        """
        if isinstance(tag, str):
            self.__tag = PgPITag(PkTag(tag, dwh).value(), dwh)
        else:
            self.__tag = tag
        self.__dwh = dwh

    def has_at(self, date: datetime) -> bool:
        raise NotImplementedError('We are not able to check now existence of a measure in a cached list')

    def last(self) -> PIMeasure:
        with self.__dwh.connection() as conn:
            row = conn.execute(text('SELECT date_pk, time_pk, millisecond, value FROM fact_pi_measure ORDER BY date_pk DESC, time_pk DESC, millisecond DESC LIMIT 1')).fetchone()
            if row is None:
                raise ValueNotFoundError('Last PI measure not found')
            return CachedPIMeasure(self.__tag, DatetimeFromPK(row[0], row[1], row[2]).value(), row[3])

    def items(self, start: datetime, end: datetime) -> list:
        result = []
        start_time = TimePK(start.time()).value()
        end_time = TimePK(end.time()).value()
        if start_time and end_time == 0:
            end_time = 235959
        with self.__dwh.connection() as conn:
            for row in conn.execute(text('SELECT date_pk, time_pk, millisecond, value FROM fact_pi_measure WHERE tag_pk = :tag_pk AND date_pk > :start AND date_pk < :end UNION ALL SELECT date_pk, time_pk, millisecond, value FROM fact_pi_measure WHERE tag_pk = :tag_pk AND ((date_pk = :start AND time_pk >= :start_time_pk) OR (date_pk = :end AND time_pk <= :end_time_pk))'), {'start': DatePK(start).value(), 'end': DatePK(end).value(), 'start_time_pk': start_time, 'end_time_pk': end_time, 'tag_pk': self.__tag.uid()}).fetchall():
                result.append(CachedPIMeasure(self.__tag, DatetimeFromPK(row[0], row[1], row[2]).value(), row[3]))
            for row in conn.execute(text('SELECT date_pk, time_pk, millisecond, value FROM fact_pi_measure_hist WHERE tag_pk = :tag_pk AND date_pk > :start AND date_pk < :end UNION ALL SELECT date_pk, time_pk, millisecond, value FROM fact_pi_measure_hist WHERE tag_pk = :tag_pk AND ((date_pk = :start AND time_pk >= :start_time_pk) OR (date_pk = :end AND time_pk <= :end_time_pk))'), {'start': DatePK(start).value(), 'end': DatePK(end).value(), 'start_time_pk': start_time, 'end_time_pk': end_time, 'tag_pk': self.__tag.uid()}).fetchall():
                result.append(CachedPIMeasure(self.__tag, DatetimeFromPK(row[0], row[1], row[2]).value(), row[3]))
        return result

    def add(self, date: datetime, value: float) -> PIMeasure:
        raise NotImplementedError("We can't add a new measure in a cached list")

class OutputDwhTableLikePIMeasures(PIMeasures):
    """
    Output PI measures like Dwh table.
    .. since: 0.6
    """

    def __init__(self, tag: PITag, writer: Writer):
        """
        Ctor.
        :param tag: Tag
        :param writer: Writer
        """
        self.__tag = tag
        self.__writer = writer

    def has_at(self, date: datetime) -> bool:
        raise NotImplementedError('Has at not supported for output PI measures')

    def last(self) -> PIMeasure:
        raise NotImplementedError('Last not supported for output PI measures')

    def items(self, start: datetime, end: datetime) -> list:
        raise NotImplementedError('Gets items not supported for output PI measures')

    def add(self, date: datetime, value: float) -> PIMeasure:
        self.__writer.write([self.__tag.uid(), DatePK(date.date()).value(), TimePK(date.time()).value(), int(date.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3].split('.')[1]), value])

class PgPIMeasuresDf(PIMeasuresDf):
    """
    PostgreSQL PI measures working with data frame.
    .. since: 0.9
    """

    def __init__(self, tag, dwh: Dwh):
        """
        Ctor.
        :param tag: Tag or code of tag
        :param dwh: Data warehouse
        """
        if isinstance(tag, str):
            self.__tag = PgPITag(PkTag(tag, dwh).value(), dwh)
        else:
            self.__tag = tag
        self.__dwh = dwh

    def frame(self, start: datetime, end: datetime) -> pd.DataFrame:
        conn = self.__dwh.connection().execution_options(stream_results=True)
        start_time = TimePK(start.time()).value()
        end_time = TimePK(end.time()).value()
        if start_time and end_time == 0:
            end_time = 235959
        result = pd.DataFrame()
        for dtf in pd.read_sql(sql=text(f"{PgPIMeasuresDf.__sql('fact_pi_measure')} UNION ALL {PgPIMeasuresDf.__sql('fact_pi_measure_hist')}"), params={'start': DatePK(start).value(), 'end': DatePK(end).value(), 'start_time_pk': start_time, 'end_time_pk': end_time, 'tag_pk': self.__tag.uid()}, con=conn, chunksize=1000, parse_dates=['datetime']):
            dtf.rename(columns={'datetime': PIMeasuresDf.DATE_TIME, 'name': PIMeasuresDf.NAME, 'value': PIMeasuresDf.VALUE}, inplace=True)
            result = pd.concat([result, dtf])
        return result

    @staticmethod
    def __sql(table: str) -> str:
        """
        SQL query for a table.
        :param table: Table name
        :return: Query
        """
        return text(f"SELECT CAST(dd.date_value AS TEXT)||'T'||dt.time_value||'.'||LPAD(mea.millisecond::text, 3, '0') || 'Z' as DateTime, mea.value as Value, tag.name as Name FROM {table} mea, dim_pi_tag tag, dim_date dd, dim_time dt WHERE mea.tag_pk = tag.tag_pk AND mea.date_pk = dd.date_pk AND mea.time_pk = dt.time_pk AND mea.tag_pk = :tag_pk AND mea.date_pk > :start AND mea.date_pk < :end UNION ALL SELECT CAST(dd.date_value AS TEXT)||'T'||dt.time_value||'.'||LPAD(mea.millisecond::text, 3, '0') || 'Z' as DateTime, mea.value as Value, tag.code as Name FROM {table} mea, dim_pi_tag tag, dim_date dd, dim_time dt WHERE mea.tag_pk = tag.tag_pk AND mea.date_pk = dd.date_pk AND mea.time_pk = dt.time_pk AND mea.tag_pk = :tag_pk AND ((mea.date_pk = :start AND mea.time_pk >= :start_time_pk) OR (mea.date_pk = :end AND mea.time_pk <= :end_time_pk))")

class PkTag:
    """
    Primary key of tag.
    .. since: 0.9
    """

    def __init__(self, code: str, dwh: Dwh):
        """
        Ctor.
        :param code: Code
        :param dwh: Data warehouse
        """
        self.__code = code
        self.__dwh = dwh

    def value(self) -> int:
        """
        # noqa: DAR401
        # noqa: DAR003
        Gets value.
        :return: Value
        :raise ValueNotFoundError: If not found
        """
        with self.__dwh.connection() as conn:
            row = conn.execute(text('SELECT tag_pk FROM dim_pi_tag WHERE code = :code'), {'code': self.__code}).fetchone()
            if row is None:
                raise ValueNotFoundError('PI tag not found')
            return row['tag_pk']