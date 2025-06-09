def deconstruct(self):
    """Serializes the :see:ConditionalUniqueIndex for the migrations file."""
    path = '%s.%s' % (self.__class__.__module__, self.__class__.__name__)
    path = path.replace('django.db.models.indexes', 'django.db.models')
    return (path, (), {'fields': self.fields, 'name': self.name, 'condition': self.condition})