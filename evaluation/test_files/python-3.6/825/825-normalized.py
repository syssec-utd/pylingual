def bulk_insert_rows(self, table, rows, target_fields=None, commit_every=5000):
    """
        A performant bulk insert for cx_Oracle
        that uses prepared statements via `executemany()`.
        For best performance, pass in `rows` as an iterator.

        :param table: target Oracle table, use dot notation to target a
            specific database
        :type table: str
        :param rows: the rows to insert into the table
        :type rows: iterable of tuples
        :param target_fields: the names of the columns to fill in the table, default None.
            If None, each rows should have some order as table columns name
        :type target_fields: iterable of str Or None
        :param commit_every: the maximum number of rows to insert in one transaction
            Default 5000. Set greater than 0. Set 1 to insert each row in each transaction
        :type commit_every: int
        """
    if not rows:
        raise ValueError('parameter rows could not be None or empty iterable')
    conn = self.get_conn()
    cursor = conn.cursor()
    values_base = target_fields if target_fields else rows[0]
    prepared_stm = 'insert into {tablename} {columns} values ({values})'.format(tablename=table, columns='({})'.format(', '.join(target_fields)) if target_fields else '', values=', '.join((':%s' % i for i in range(1, len(values_base) + 1))))
    row_count = 0
    row_chunk = []
    for row in rows:
        row_chunk.append(row)
        row_count += 1
        if row_count % commit_every == 0:
            cursor.prepare(prepared_stm)
            cursor.executemany(None, row_chunk)
            conn.commit()
            self.log.info('[%s] inserted %s rows', table, row_count)
            row_chunk = []
    cursor.prepare(prepared_stm)
    cursor.executemany(None, row_chunk)
    conn.commit()
    self.log.info('[%s] inserted %s rows', table, row_count)
    cursor.close()
    conn.close()