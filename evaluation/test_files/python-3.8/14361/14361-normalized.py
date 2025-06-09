def draw_titles(self):
    """Draws the graph title and subtitle"""
    if self.show_graph_title:
        self.draw_graph_title()
    if self.show_graph_subtitle:
        self.draw_graph_subtitle()
    if self.show_x_title:
        self.draw_x_title()
    if self.show_y_title:
        self.draw_y_title()