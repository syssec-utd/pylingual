def create_widget(self):
    """ Create the toolkit widget for the proxy object.

        This method is called during the top-down pass, just before the
        'init_widget()' method is called. This method should create the
        toolkit widget and assign it to the 'widget' attribute.

        """
    self.widget = SubElement(self.parent_widget(), self.declaration.tag)