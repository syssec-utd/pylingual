from odoo.tools import query
Oridinal_Query_obj = query.Query

def percent_search_fuzzy(self, where_claus):
    if ' % ' in ' '.join(where_claus):
        new_where_clause = [x.replace(' % ', ' %% ') for x in where_claus]
        return tuple(new_where_clause)
    return where_claus
Oridinal_Query_obj.percent_search_fuzzy = percent_search_fuzzy

def where_clause_new(self):
    ok_where = self.percent_search_fuzzy(self._where_clausess)
    return tuple(ok_where)
Oridinal_Query_obj.where_clause = where_clause_new

def get_sql_new(self):
    """Returns (query_from, query_where, query_params)."""
    tables = [query._from_table(table, alias) for (alias, table) in self._tables.items()]
    joins = []
    params = []
    for (alias, (kind, table, condition, condition_params)) in self._joins.items():
        joins.append(f'{kind} {query._from_table(table, alias)} ON ({condition})')
        params.extend(condition_params)
    from_clause = ' '.join([', '.join(tables)] + joins)
    ok_where = self.percent_search_fuzzy(self._where_clauses)
    where_clause = ' AND '.join(ok_where)
    return (from_clause, where_clause, params + self._where_params)
Oridinal_Query_obj.get_sql = get_sql_new