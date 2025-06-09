from django.core.exceptions import FieldError
from django.db.models.expressions import Col
from django.db.models.sql import compiler

class SQLCompiler(compiler.SQLCompiler):

    def as_subquery_condition(self, alias, columns, compiler):
        qn = compiler.quote_name_unless_alias
        qn2 = self.connection.ops.quote_name
        sql, params = self.as_sql()
        return ('(%s) IN (%s)' % (', '.join(('%s.%s' % (qn(alias), qn2(column)) for column in columns)), sql), params)

class SQLInsertCompiler(compiler.SQLInsertCompiler, SQLCompiler):
    pass

class SQLDeleteCompiler(compiler.SQLDeleteCompiler, SQLCompiler):

    def as_sql(self):
        where, having = self.query.where.split_having()
        if self.single_alias or having:
            return super().as_sql()
        result = ['DELETE %s FROM' % self.quote_name_unless_alias(self.query.get_initial_alias())]
        from_sql, from_params = self.get_from_clause()
        result.extend(from_sql)
        where_sql, where_params = self.compile(where)
        if where_sql:
            result.append('WHERE %s' % where_sql)
        return (' '.join(result), tuple(from_params) + tuple(where_params))

class SQLUpdateCompiler(compiler.SQLUpdateCompiler, SQLCompiler):

    def as_sql(self):
        update_query, update_params = super().as_sql()
        if self.query.order_by:
            order_by_sql = []
            order_by_params = []
            db_table = self.query.get_meta().db_table
            try:
                for resolved, (sql, params, _) in self.get_order_by():
                    if isinstance(resolved.expression, Col) and resolved.expression.alias != db_table:
                        raise FieldError
                    order_by_sql.append(sql)
                    order_by_params.extend(params)
                update_query += ' ORDER BY ' + ', '.join(order_by_sql)
                update_params += tuple(order_by_params)
            except FieldError:
                pass
        return (update_query, update_params)

class SQLAggregateCompiler(compiler.SQLAggregateCompiler, SQLCompiler):
    pass