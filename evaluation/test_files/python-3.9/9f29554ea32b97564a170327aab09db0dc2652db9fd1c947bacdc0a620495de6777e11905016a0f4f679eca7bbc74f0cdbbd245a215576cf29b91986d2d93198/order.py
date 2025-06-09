from ..base_sql_expression import BaseSqlExpression
from ..column.column_ordering import BaseColumnOrdering
from ..sql_value_type import SqlValType

class WindowOrder(BaseSqlExpression):
    """Class that represents the ordering part of the OVER clause in a SQL window function.

    """

    def __init__(self, *orders: BaseColumnOrdering):
        """Constructor of the window order class

        Args:
            *orders (BaseColumnOrdering): ordering to apply to the window.
        """
        if len(orders) == 0:
            raise ValueError('WindowOrder must receive at least one ordering expression. Received zero.')
        if any((not isinstance(o, BaseColumnOrdering) for o in orders)):
            raise TypeError('All arguments to the WindowOrder must be orderings. Try calling ascending() on the column')
        super().__init__('window ordering', lambda *args: f"ORDER BY {', '.join((a.get_sql() for a in args))}", lambda *args: all((a == SqlValType.Ordering for a in args)), lambda *args: SqlValType.ColumnSelection, *orders)