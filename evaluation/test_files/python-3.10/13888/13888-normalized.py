def get_table(self, items):
    """Generate a proper list of table nodes for autosummary:: directive.

        *items* is a list produced by :meth:`get_items`.
        """
    table_spec = addnodes.tabular_col_spec()
    table_spec['spec'] = 'll'
    table = autosummary_table('')
    real_table = nodes.table('', classes=['longtable'])
    table.append(real_table)
    group = nodes.tgroup('', cols=2)
    real_table.append(group)
    group.append(nodes.colspec('', colwidth=10))
    group.append(nodes.colspec('', colwidth=90))
    body = nodes.tbody('')
    group.append(body)

    def append_row(*column_texts):
        row = nodes.row('')
        for text in column_texts:
            node = nodes.paragraph('')
            vl = ViewList()
            vl.append(text, '<autosummary>')
            self.state.nested_parse(vl, 0, node)
            try:
                if isinstance(node[0], nodes.paragraph):
                    node = node[0]
            except IndexError:
                pass
            row.append(nodes.entry('', node))
        body.append(row)
    for (name, sig, summary, real_name) in items:
        qualifier = 'obj'
        if 'nosignatures' not in self.options:
            col1 = ':%s:`%s <%s>`\\ %s' % (qualifier, name, real_name, sig)
        else:
            col1 = ':%s:`%s <%s>`' % (qualifier, name, real_name)
        col2 = summary
        append_row(col1, col2)
    return [table_spec, table]