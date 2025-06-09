"""颜色表示"""

class Color(object):
    """以 0-255 的整数表示颜色值, 不提供序列化方法"""

    def __init__(self, red: int=0, green: int=0, blue: int=0):
        if red > 255:
            raise ValueError('red must be 0-255')
        if green > 255:
            raise ValueError('green must be 0-255')
        if blue > 255:
            raise ValueError('blue must be 0-255')
        self.red = red
        self.green = green
        self.blue = blue

class Alpha(object):
    """以 0-255 的整数表示透明度, 255 是不透明, 不提供序列化方法"""

    def __init__(self, alpha: int=0):
        if alpha > 255:
            raise ValueError('alpha must be 0-255')
        self.alpha = alpha

class Rgba(object):

    def __init__(self, color: Color=Color(), alpha: Alpha=Alpha()):
        self.color = color
        self.alpha = alpha