def load_class(full_class_string):
    """Loads a class from a string naming the module and class name.

    For example:
    >>> load_class(full_class_string = 'pypet.brian.parameter.BrianParameter')
    <BrianParameter>

    """
    class_data = full_class_string.split('.')
    module_path = '.'.join(class_data[:-1])
    class_str = class_data[-1]
    module = importlib.import_module(module_path)
    return getattr(module, class_str)