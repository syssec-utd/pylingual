def select_many(self, kind, *args):
    """
        Query the metamodel for a set of instances of some *kind*. Query
        operators such as where_eq(), order_by() or filter functions may be
        passed as optional arguments.
        
        Usage example:
        
        >>> m = xtuml.load_metamodel('db.sql')
        >>> inst_set = m.select_many('My_Class', lambda sel: sel.number > 5)
        """
    metaclass = self.find_metaclass(kind)
    return metaclass.select_many(*args)