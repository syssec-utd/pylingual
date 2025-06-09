import numpy as np
from matplotlib.path import Path

class BinaryRenderer:

    def __init__(self, size, fill_value: bool=False) -> None:
        self.map = np.full(size, fill_value=fill_value, dtype=bool)
        self.xx, self.yy = np.meshgrid(range(size[1]), range(size[0]))
        self.xy = np.vstack((self.xx.flatten(), self.yy.flatten())).T

    def circle(self, x, y, radius, value=True) -> None:
        x0 = max(int(x - radius), 0)
        y0 = max(int(y - radius), 0)
        x1 = min(int(x + radius) + 2, self.map.shape[1] - 1)
        y1 = min(int(y + radius) + 2, self.map.shape[0] - 1)
        roi = self.map[y0:y1, x0:x1]
        sqr_dist = (self.xx[y0:y1, x0:x1] - x) ** 2 + (self.yy[y0:y1, x0:x1] - y) ** 2
        roi[sqr_dist <= radius ** 2] = value
        self.map[y0:y1, x0:x1] = roi

    def polygon(self, points, value=True) -> None:
        if len(points) == 0:
            return
        x0 = max(int(points[:, 0].min()), 0)
        y0 = max(int(points[:, 1].min()), 0)
        x1 = min(int(points[:, 0].max()) + 2, self.map.shape[1] - 1)
        y1 = min(int(points[:, 1].max()) + 2, self.map.shape[0] - 1)
        xy = np.vstack((self.xx[y0:y1, x0:x1].flatten(), self.yy[y0:y1, x0:x1].flatten())).T
        roi = self.map[y0:y1, x0:x1]
        roi[Path(points).contains_points(xy).reshape(roi.shape)] = value
        self.map[y0:y1, x0:x1] = roi