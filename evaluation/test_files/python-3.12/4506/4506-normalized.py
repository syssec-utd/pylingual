def get_level_str(self):
    """ format level str """
    if self.is_relative:
        level_str = str(self.level) + '%'
    else:
        level_str = self.level
    return level_str