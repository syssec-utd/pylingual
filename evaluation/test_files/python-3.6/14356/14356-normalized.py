def make_datapoint_text(self, x, y, value, style=None):
    """
		Add text for a datapoint
		"""
    if not self.show_data_values:
        return
    e = etree.SubElement(self.foreground, 'text', {'x': str(x), 'y': str(y), 'class': 'dataPointLabel', 'style': '%(style)s stroke: #fff; stroke-width: 2;' % vars()})
    e.text = str(value)
    e = etree.SubElement(self.foreground, 'text', {'x': str(x), 'y': str(y), 'class': 'dataPointLabel'})
    e.text = str(value)
    if style:
        e.set('style', style)