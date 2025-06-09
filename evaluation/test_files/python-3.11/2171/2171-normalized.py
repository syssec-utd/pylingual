def upload_custom_metric(func, func_file='metrics.py', func_name=None, class_name=None, source_provider=None):
    """
    Upload given metrics function into H2O cluster.

    The metrics can have different representation:
      - class: needs to implement map(pred, act, weight, offset, model), reduce(l, r) and metric(l) methods
      - string: the same as in class case, but the class is given as a string

    :param func:  metric representation: string, class
    :param func_file:  internal name of file to save given metrics representation
    :param func_name:  name for h2o key under which the given metric is saved
    :param class_name: name of class wrapping the metrics function (when supplied as string)
    :param source_provider: a function which provides a source code for given function
    :return: reference to uploaded metrics function

    :examples:
        >>> class CustomMaeFunc:
        >>>     def map(self, pred, act, w, o, model):
        >>>         return [abs(act[0] - pred[0]), 1]
        >>>
        >>>     def reduce(self, l, r):
        >>>         return [l[0] + r[0], l[1] + r[1]]
        >>>
        >>>     def metric(self, l):
        >>>         return l[0] / l[1]
        >>>
        >>>
        >>> h2o.upload_custom_metric(CustomMaeFunc, func_name="mae")
        >>>
        >>> custom_func_str = '''class CustomMaeFunc:
        >>>     def map(self, pred, act, w, o, model):
        >>>         return [abs(act[0] - pred[0]), 1]
        >>>
        >>>     def reduce(self, l, r):
        >>>         return [l[0] + r[0], l[1] + r[1]]
        >>>
        >>>     def metric(self, l):
        >>>         return l[0] / l[1]'''
        >>>
        >>>
        >>> h2o.upload_custom_metric(custom_func_str, class_name="CustomMaeFunc", func_name="mae")
    """
    import tempfile
    import inspect
    if not source_provider:
        source_provider = _default_source_provider
    _CFUNC_CODE_TEMPLATE = '# Generated code\nimport water.udf.CMetricFunc as MetricFunc\n\n# User given metric function as a class implementing\n# 3 methods defined by interface CMetricFunc\n{}\n\n# Generated user metric which satisfies the interface\n# of Java MetricFunc\nclass {}Wrapper({}, MetricFunc, object):\n    pass\n\n'
    assert_satisfies(func, inspect.isclass(func) or isinstance(func, str), 'The argument func needs to be string or class !')
    assert_satisfies(func_file, func_file is not None, 'The argument func_file is missing!')
    assert_satisfies(func_file, func_file.endswith('.py'), "The argument func_file needs to end with '.py'")
    code = None
    derived_func_name = None
    module_name = func_file[:-3]
    if isinstance(func, str):
        assert_satisfies(class_name, class_name is not None, 'The argument class_name is missing! ' + 'It needs to reference the class in given string!')
        code = _CFUNC_CODE_TEMPLATE.format(func, class_name, class_name)
        derived_func_name = 'metrics_{}'.format(class_name)
        class_name = '{}.{}Wrapper'.format(module_name, class_name)
    else:
        assert_satisfies(func, inspect.isclass(func), 'The parameter `func` should be str or class')
        for method in ['map', 'reduce', 'metric']:
            assert_satisfies(func, method in func.__dict__, 'The class `func` needs to define method `{}`'.format(method))
        assert_satisfies(class_name, class_name is None, 'If class is specified then class_name parameter needs to be None')
        class_name = '{}.{}Wrapper'.format(module_name, func.__name__)
        derived_func_name = 'metrics_{}'.format(func.__name__)
        code = _CFUNC_CODE_TEMPLATE.format(source_provider(func), func.__name__, func.__name__)
    if not func_name:
        func_name = derived_func_name
    tmpdir = tempfile.mkdtemp(prefix='h2o-func')
    func_arch_file = _create_zip_file('{}/func.jar'.format(tmpdir), (func_file, code))
    dest_key = _put_key(func_arch_file, dest_key=func_name)
    return 'python:{}={}'.format(dest_key, class_name)