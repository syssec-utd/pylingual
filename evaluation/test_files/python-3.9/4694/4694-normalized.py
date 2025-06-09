def _find_class_construction_fn(cls):
    """Find the first __init__ or __new__ method in the given class's MRO."""
    for base in type.mro(cls):
        if '__init__' in base.__dict__:
            return base.__init__
        if '__new__' in base.__dict__:
            return base.__new__