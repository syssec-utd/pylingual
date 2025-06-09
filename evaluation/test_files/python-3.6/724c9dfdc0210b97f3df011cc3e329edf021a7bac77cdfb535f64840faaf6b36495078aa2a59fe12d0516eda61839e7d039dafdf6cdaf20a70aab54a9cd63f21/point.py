from typing import Optional, Tuple, Union, List, Sequence, Iterable
from itertools import chain
import attrs
import numpy as np
from .type import Shapable
from .opt import extract_shape_from_shapable_or_shape, clip_val, resize_val, generate_shape_and_resized_shape
_T = Union[float, str]

@attrs.define(frozen=True)
class Point:
    smooth_y: float = attrs.field(eq=False)
    smooth_x: float = attrs.field(eq=False)
    y: int = attrs.field(init=False, hash=False)
    x: int = attrs.field(init=False, hash=False)

    def __attrs_post_init__(self):
        object.__setattr__(self, 'y', round(self.smooth_y))
        object.__setattr__(self, 'x', round(self.smooth_x))

    @classmethod
    def create(cls, y: _T, x: _T):
        return cls(smooth_y=float(y), smooth_x=float(x))

    @classmethod
    def from_xy_pair(cls, xy_pair: Tuple[_T, _T]):
        (x, y) = xy_pair
        return cls.create(y=y, x=x)

    def to_xy_pair(self):
        return (self.x, self.y)

    def to_smooth_xy_pair(self):
        return (self.smooth_x, self.smooth_y)

    def to_clipped_point(self, shapable_or_shape: Union[Shapable, Tuple[int, int]]):
        (height, width) = extract_shape_from_shapable_or_shape(shapable_or_shape)
        if 0 <= self.y < height and 0 <= self.x < width:
            return self
        else:
            return Point.create(y=clip_val(self.smooth_y, height), x=clip_val(self.smooth_x, width))

    def to_shifted_point(self, offset_y: int=0, offset_x: int=0):
        return Point.create(y=self.smooth_y + offset_y, x=self.smooth_x + offset_x)

    def to_conducted_resized_point(self, shapable_or_shape: Union[Shapable, Tuple[int, int]], resized_height: Optional[int]=None, resized_width: Optional[int]=None):
        (height, width, resized_height, resized_width) = generate_shape_and_resized_shape(shapable_or_shape=shapable_or_shape, resized_height=resized_height, resized_width=resized_width)
        return Point.create(y=resize_val(self.smooth_y, height, resized_height), x=resize_val(self.smooth_x, width, resized_width))

class PointList(List[Point]):

    @classmethod
    def from_point(cls, point: Point):
        return cls((point,))

    @classmethod
    def from_xy_pairs(cls, xy_pairs: Iterable[Tuple[_T, _T]]):
        return cls((Point.from_xy_pair(xy_pair) for xy_pair in xy_pairs))

    def to_xy_pairs(self):
        return [point.to_xy_pair() for point in self]

    def to_smooth_xy_pairs(self):
        return [point.to_smooth_xy_pair() for point in self]

    @classmethod
    def from_flatten_xy_pairs(cls, flatten_xy_pairs: Sequence[_T]):
        flatten_xy_pairs = tuple(flatten_xy_pairs)
        assert flatten_xy_pairs and len(flatten_xy_pairs) % 2 == 0
        points = PointList()
        idx = 0
        while idx < len(flatten_xy_pairs):
            x = flatten_xy_pairs[idx]
            y = flatten_xy_pairs[idx + 1]
            points.append(Point.create(y=y, x=x))
            idx += 2
        return points

    def to_flatten_xy_pairs(self):
        return list(chain.from_iterable((point.to_xy_pair() for point in self)))

    def to_smooth_flatten_xy_pairs(self):
        return list(chain.from_iterable((point.to_smooth_xy_pair() for point in self)))

    @classmethod
    def from_np_array(cls, np_points: np.ndarray):
        points = PointList()
        for np_point in np_points:
            (x, y) = np_point
            points.append(Point.create(y=y, x=x))
        if len(points) > 2 and points[0] == points[-1]:
            points.pop()
        return points

    def to_np_array(self):
        return np.asarray(self.to_xy_pairs(), dtype=np.int32)

    def to_smooth_np_array(self):
        return np.asarray(self.to_smooth_xy_pairs(), dtype=np.float32)

    def to_point_tuple(self):
        return PointTuple(self)

    def copy(self):
        return PointList(self)

    def to_clipped_points(self, shapable_or_shape: Union[Shapable, Tuple[int, int]]):
        return PointList((point.to_clipped_point(shapable_or_shape) for point in self))

    def to_shifted_points(self, offset_y: int=0, offset_x: int=0):
        return PointList((point.to_shifted_point(offset_y=offset_y, offset_x=offset_x) for point in self))

    def to_relative_points(self, origin_y: int, origin_x: int):
        return self.to_shifted_points(offset_y=-origin_y, offset_x=-origin_x)

    def to_conducted_resized_points(self, shapable_or_shape: Union[Shapable, Tuple[int, int]], resized_height: Optional[int]=None, resized_width: Optional[int]=None):
        return PointList((point.to_conducted_resized_point(shapable_or_shape=shapable_or_shape, resized_height=resized_height, resized_width=resized_width) for point in self))

class PointTuple(Tuple[Point, ...]):

    @classmethod
    def from_point(cls, point: Point):
        return cls((point,))

    @classmethod
    def from_xy_pairs(cls, xy_pairs: Iterable[Tuple[_T, _T]]):
        return PointTuple((Point.from_xy_pair(xy_pair) for xy_pair in xy_pairs))

    def to_xy_pairs(self):
        return tuple((point.to_xy_pair() for point in self))

    def to_smooth_xy_pairs(self):
        return tuple((point.to_smooth_xy_pair() for point in self))

    @classmethod
    def from_flatten_xy_pairs(cls, flatten_xy_pairs: Sequence[_T]):
        return PointList.from_flatten_xy_pairs(flatten_xy_pairs).to_point_tuple()

    def to_flatten_xy_pairs(self):
        return tuple(chain.from_iterable((point.to_xy_pair() for point in self)))

    def to_smooth_flatten_xy_pairs(self):
        return tuple(chain.from_iterable((point.to_smooth_xy_pair() for point in self)))

    @classmethod
    def from_np_array(cls, np_points: np.ndarray):
        return PointList.from_np_array(np_points).to_point_tuple()

    def to_np_array(self):
        return np.asarray(self.to_xy_pairs(), dtype=np.int32)

    def to_smooth_np_array(self):
        return np.asarray(self.to_xy_pairs(), dtype=np.float32)

    def to_clipped_points(self, shapable_or_shape: Union[Shapable, Tuple[int, int]]):
        return PointTuple((point.to_clipped_point(shapable_or_shape) for point in self))

    def to_shifted_points(self, offset_y: int=0, offset_x: int=0):
        return PointTuple((point.to_shifted_point(offset_y=offset_y, offset_x=offset_x) for point in self))

    def to_relative_points(self, origin_y: int, origin_x: int):
        return self.to_shifted_points(offset_y=-origin_y, offset_x=-origin_x)

    def to_conducted_resized_points(self, shapable_or_shape: Union[Shapable, Tuple[int, int]], resized_height: Optional[int]=None, resized_width: Optional[int]=None):
        return PointTuple((point.to_conducted_resized_point(shapable_or_shape=shapable_or_shape, resized_height=resized_height, resized_width=resized_width) for point in self))