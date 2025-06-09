def set_page_size(self, layout):
    """ Valid choices: 'a3, 'a4', 'a5', 'letter', 'legal', '11x17'.

        """
    self.layout = layout.lower()
    if self.layout in self.layout_dict:
        self.page_size = self.layout_dict[self.layout]
    else:
        dimensions = self.layout.split('x')
        if len(dimensions) == 2:
            self.page_size = (float(dimensions[0]) * 72, float(dimensions[1]) * 72)
        else:
            raise IndexError('Page is two dimensions, given: %s' % len(dimensions))