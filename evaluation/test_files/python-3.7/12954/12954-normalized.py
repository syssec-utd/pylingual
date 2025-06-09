def way(self, w):
    """Process each way."""
    if w.id not in self.way_ids:
        return
    way_points = []
    for n in w.nodes:
        try:
            way_points.append(Point(n.location.lon, n.location.lat))
        except o.InvalidLocationError:
            logging.debug('InvalidLocationError at way %s node %s', w.id, n.ref)
    self.ways[w.id] = Way(w.id, way_points)