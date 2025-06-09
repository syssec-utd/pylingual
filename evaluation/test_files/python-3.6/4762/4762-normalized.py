def remove_property(self, property_):
    """
        Remove a property from this thing.

        property_ -- property to remove
        """
    if property_.name in self.properties:
        del self.properties[property_.name]