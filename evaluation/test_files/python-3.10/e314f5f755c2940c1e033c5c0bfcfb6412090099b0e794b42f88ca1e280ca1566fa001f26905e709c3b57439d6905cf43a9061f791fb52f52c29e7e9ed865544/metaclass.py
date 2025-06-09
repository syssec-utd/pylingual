__author__ = 'wsb310@gmail.com'
import threading
import traceback

class SafeSingletonMetaclass(type):
    """线程安全的单例的元类实现
    """

    def __init__(cls, _what, _bases=None, _dict=None):
        super().__init__(_what, _bases, _dict)
        cls._instance = None
        cls._lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        result = None
        cls._lock.acquire()
        try:
            if cls._instance is not None:
                result = cls._instance
            else:
                result = cls._instance = super().__call__(*args, **kwargs)
        except Exception as _:
            traceback.print_exc()
        finally:
            cls._lock.release()
        return result

class SafeSingleton(metaclass=SafeSingletonMetaclass):
    """线程安全的单例基类
    """
    pass

class SingletonMetaclass(type):
    """单例的元类实现
    """

    def __init__(cls, _what, _bases=None, _dict=None):
        super().__init__(_what, _bases, _dict)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        result = None
        try:
            if cls._instance is not None:
                result = cls._instance
            else:
                result = cls._instance = super().__call__(*args, **kwargs)
        except Exception as _:
            traceback.print_exc()
        return result

class Singleton(metaclass=SingletonMetaclass):
    """单例基类
    """
    pass

class SubclassMetaclass(type):
    """子类清单

    该元类的类，能感知自身被继承，并提供子类清单

    """
    _baseclasses = []

    def __new__(mcs, name, bases, attrs):
        subclass = '.'.join([attrs['__module__'], attrs['__qualname__']])
        for base in bases:
            if base in mcs._baseclasses:
                getattr(base, '_subclasses').append(subclass)
            else:
                mcs._baseclasses.append(base)
                setattr(base, '_subclasses', [subclass])
        return type.__new__(mcs, name, bases, attrs)