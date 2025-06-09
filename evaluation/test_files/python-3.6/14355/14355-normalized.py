def draw_graph(self):
    """
		The central logic for drawing the graph.

		Sets self.graph (the 'g' element in the SVG root)
		"""
    transform = 'translate (%s %s)' % (self.border_left, self.border_top)
    self.graph = etree.SubElement(self.root, 'g', transform=transform)
    etree.SubElement(self.graph, 'rect', {'x': '0', 'y': '0', 'width': str(self.graph_width), 'height': str(self.graph_height), 'class': 'graphBackground'})
    etree.SubElement(self.graph, 'path', {'d': 'M 0 0 v%s' % self.graph_height, 'class': 'axis', 'id': 'xAxis'})
    etree.SubElement(self.graph, 'path', {'d': 'M 0 %s h%s' % (self.graph_height, self.graph_width), 'class': 'axis', 'id': 'yAxis'})
    self.draw_x_labels()
    self.draw_y_labels()