def create_foundation(length, width, depth=0.0, height=0.0):
    """
    Can define a Foundation Object from dimensions.
    :param length: Foundation length
    :param width: Foundation width
    :param depth: Foundation depth
    :param height: Foundation height
    :return: A Foundation object
    """
    a_foundation = FoundationRaft()
    a_foundation.length = length
    a_foundation.width = width
    a_foundation.depth = depth
    a_foundation.height = height
    return a_foundation