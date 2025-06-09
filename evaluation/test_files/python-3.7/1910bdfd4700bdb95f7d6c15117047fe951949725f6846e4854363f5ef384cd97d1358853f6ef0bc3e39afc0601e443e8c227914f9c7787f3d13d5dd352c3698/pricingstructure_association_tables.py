from typing import List
from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.sqlite_table import SqliteTable
__all__ = ['TablePricingStructuresTariffs']

class TablePricingStructuresTariffs(SqliteTable):
    pricing_structure_mrid: Column = None
    tariff_mrid: Column = None

    def __init__(self):
        super(TablePricingStructuresTariffs, self).__init__()
        self.pricing_structure_mrid = self._create_column('pricing_structure_mrid', 'TEXT', Nullable.NOT_NULL)
        self.tariff_mrid = self._create_column('tariff_mrid', 'TEXT', Nullable.NOT_NULL)

    def name(self) -> str:
        return 'pricing_structures_tariffs'

    def unique_index_columns(self) -> List[List[Column]]:
        cols = super(TablePricingStructuresTariffs, self).unique_index_columns()
        cols.append([self.pricing_structure_mrid, self.tariff_mrid])
        return cols

    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super(TablePricingStructuresTariffs, self).non_unique_index_columns()
        cols.append([self.pricing_structure_mrid])
        cols.append([self.tariff_mrid])
        return cols