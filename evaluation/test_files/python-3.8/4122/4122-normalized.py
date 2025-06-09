def dist_abs(self):
    """Distance abs
        """
    bounds = self.ax.get_xlim() if self.x else self.ax.get_ylim()
    return bounds[0] - bounds[1]