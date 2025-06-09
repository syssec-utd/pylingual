from abc import ABCMeta

class SingletonMetaclass(ABCMeta):
    """
    Overview:
        Returns the given type instance in input class
    Interface:
        ``__call__``
    """
    instances = {}

    def __call__(cls: type, *args, **kwargs) -> object:
        if cls not in SingletonMetaclass.instances:
            SingletonMetaclass.instances[cls] = super(SingletonMetaclass, cls).__call__(*args, **kwargs)
            cls.instance = SingletonMetaclass.instances[cls]
        return SingletonMetaclass.instances[cls]