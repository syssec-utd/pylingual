from __future__ import annotations
from typing import Any, TYPE_CHECKING, Union
import QuantLib as ql
from valuation.consts import signatures
from valuation.consts import fields
from valuation.engine.utility_objects import QLUtilityObject
if TYPE_CHECKING:
    from valuation.engine import QLObjectDB
    from valuation.engine.mappings import QLBusiness
    from valuation.universal_transfer import Storage, DefaultParameters

class QLDateRoller(QLUtilityObject):
    _signature = signatures.utilities.date_roller

    def __init__(self, data: Storage, ql_db: QLObjectDB, default_parameters: DefaultParameters, data_only_mode: bool=False) -> None:
        super().__init__(data, ql_db, default_parameters, data_only_mode)
        self.business: QLBusiness = self.data(fields.Business)
        self.calendar: ql.Calendar = self.data(fields.Calendar)
        self.date: ql.Date = self.data(fields.Date)

    def get_raw_data(self) -> Union[dict[str, Any], list[dict[str, Any]]]:
        return self.calendar.advance(self.date, ql.Period(0, ql.Days), self.business).ISO()