import functools
from archaea.geometry.line_segment import LineSegment
from archaea.geometry.point3d import Point3d

class Polyline:
    points: 'list[Point3d]'

    def __init__(self, points: 'list[Point3d]'):
        self.points = points

    @functools.cached_property
    def segments(self):
        consecutive_pairs = [[self.points[i], self.points[i + 1]] for i in range(len(self.points) - 1)]
        return [LineSegment(start, end) for [start, end] in consecutive_pairs]

    @functools.cached_property
    def segment_count(self):
        return len(self.segments)

    @functools.cached_property
    def length(self):
        return sum((segment.length for segment in self.segments))

    @functools.cached_property
    def point_at_start(self) -> Point3d:
        return self.segments[0].start

    @functools.cached_property
    def point_at_end(self) -> Point3d:
        return self.segments[-1].end

    @functools.cached_property
    def is_closed(self):
        return self.point_at_start == self.point_at_end