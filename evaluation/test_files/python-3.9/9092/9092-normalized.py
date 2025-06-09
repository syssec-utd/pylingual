def set_source(self, source):
    """ Set the source by parsing the source and inserting it into the 
        component. 
        """
    self.widget.clear()
    html = etree.HTML(source)
    self.widget.extend(html[0])
    super(RawComponent, self).init_widget()