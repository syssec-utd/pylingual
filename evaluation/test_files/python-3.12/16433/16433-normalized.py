def parse_xdot_label_directive(self, new):
    """ Parses the label drawing directive, updating the label
            components.
        """
    components = XdotAttrParser().parse_xdot_data(new)
    pos_x = min([c.x for c in components])
    pos_y = min([c.y for c in components])
    move_to_origin(components)
    container = Container(auto_size=True, position=[pos_x - self.pos[0], pos_y - self.pos[1]], bgcolor='red')
    container.add(*components)
    self.label_drawing = container