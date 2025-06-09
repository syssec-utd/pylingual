def node_factory(**row_factory_kw):
    """ Give new nodes a unique ID. """
    if '__table_editor__' in row_factory_kw:
        graph = row_factory_kw['__table_editor__'].object
        ID = make_unique_name('n', [node.ID for node in graph.nodes])
        del row_factory_kw['__table_editor__']
        return godot.node.Node(ID)
    else:
        return godot.node.Node(uuid.uuid4().hex[:6])