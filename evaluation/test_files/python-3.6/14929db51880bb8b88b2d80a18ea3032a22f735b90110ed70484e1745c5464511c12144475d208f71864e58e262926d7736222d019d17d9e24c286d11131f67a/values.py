import numpy as np
import copy
import json
from sklearn.pipeline import make_pipeline
from river import compose
from spotPython.utils.convert import class_for_name
from spotPython.utils.transform import transform_hyper_parameter_values

def generate_one_config_from_var_dict(var_dict, fun_control) -> dict:
    """Generate one configuration from a dictionary of variables (as a generator).
    This function takes a dictionary of variables as input arguments and returns a dictionary
    with the values from the arrays in the dictionary.
    Args:
        var_dict (dict): A dictionary where keys are variable names and values are numpy arrays.
        fun_control (dict): A dictionary which (at least) has an entry with the following key:
            - "var_type": A list of variable types. If the entry is not "num" the corresponding
            value will be converted to the type "int".
    Returns:
        dict: A dictionary with the values from the arrays in the dictionary.
    Example:
        >>> import numpy as np
        >>> var_dict = {'a': np.array([1, 3, 5]), 'b': np.array([2, 4, 6])}
        >>> fun_control = {"var_type": ["int", "num"]}
        >>> generate_one_config_from_var_dict(var_dict, fun_control)
        {'a': 1, 'b': 2}
    """
    for values in iterate_dict_values(var_dict):
        values = convert_keys(values, fun_control['var_type'])
        values = get_dict_with_levels_and_types(fun_control=fun_control, v=values)
        values = transform_hyper_parameter_values(fun_control=fun_control, hyper_parameter_values=values)
        yield values

def return_conf_list_from_var_dict(var_dict: dict, fun_control: dict) -> list:
    """This function takes a dictionary of variables and a dictionary of function control.
    It performs similar steps as generate_one_config_from_var_dict()
    but returns a list of dictionaries of hyper parameter values.
    Args:
        var_dict (dict): A dictionary of variables.
        fun_control (dict): A dictionary of function control.
    Returns:
        list A list of dictionaries of hyper parameter values. Transformations are applied to the values.
    Examples:
        >>> import numpy as np
            var_dict = {'a': np.array([1]),
                        'b': np.array([2])}
            fun_control = {'var_type': ['int', 'int']}
            return_conf_list_from_var_dict(var_dict, fun_control)
            var_dict = {'a': np.array([1, 3, 5]), 'b': np.array([2, 4, 6])}
            fun_control = {'var_type': ['int', 'int']}
            return_conf_list_from_var_dict(var_dict, fun_control)
            {'a': [1, 3, 5], 'b': [2, 4, 6]}

    """
    conf_list = []
    for values in generate_one_config_from_var_dict(var_dict, fun_control):
        conf_list.append(values)
    return conf_list

def iterate_dict_values(var_dict: dict):
    """
    This function takes a dictionary of variables as input arguments and returns an iterator that
    yields the values from the arrays in the dictionary.

    Parameters:
        var_dict (dict): A dictionary where keys are variable names and values are numpy arrays.

    Returns:
        iterator: An iterator that yields the values from the arrays in the dictionary.

    Example:
        >>> import numpy as np
        >>> var_dict = {'a': np.array([1, 3, 5]), 'b': np.array([2, 4, 6])}
        >>> for values in iterate_dict_values(var_dict):
        ...     print(values)
        {'a': 1, 'b': 2}
        {'a': 3, 'b': 4}
        {'a': 5, 'b': 6}
    """
    n = len(next(iter(var_dict.values())))
    for i in range(n):
        yield {key: value[i] for (key, value) in var_dict.items()}

def convert_keys(d: dict, var_type: list):
    """
    Convert values in a dictionary to integers based on a list of variable types.

    This function takes a dictionary `d` and a list of variable types `var_type` as arguments.
    For each key in the dictionary,
    if the corresponding entry in `var_type` is not equal to `"num"`,
    the value associated with that key is converted to an integer.

    Args:
        d (dict): The input dictionary.
        var_type (list): A list of variable types. If the entry is not `"num"` the corresponding
        value will be converted to the type `"int"`.

    Returns:
        dict: The modified dictionary with values converted to integers based on `var_type`.

    Example:
        >>> d = {'a': '1.1', 'b': '2', 'c': '3.1'}
        >>> var_type = ["int", "num", "int"]
        >>> convert_keys(d, var_type)
        {'a': 1, 'b': '2', 'c': 3}
    """
    keys = list(d.keys())
    for i in range(len(keys)):
        if var_type[i] not in ['num', 'float']:
            d[keys[i]] = int(d[keys[i]])
    return d

def get_dict_with_levels_and_types(fun_control, v) -> dict:
    """Get dictionary with levels and types.
    The function maps the numerical output of the hyperparameter optimization to the corresponding levels
    of the hyperparameter needed by the core model, i.e., the tuned algorithm.
    The function takes the dictionaries fun_control and v and returns a new dictionary with the same keys as v
    but with the values of the levels of the keys from fun_control.
    If the key value in the dictionary is 0, it takes the first value from the list,
    if it is 1, it takes the second and so on.
    If a key is not in fun_control, it takes the key from v.
    If the core_model_parameter_type value is instance, it returns the class of the value from the module
    via getattr("class", value).
    For example,
    if fun_control = {"HoeffdingTreeRegressor":{
        "leaf_prediction": {
            "levels": ["mean", "model", "adaptive"],
            "type": "factor",
            "default": "mean",
            "core_model_parameter_type": "str"},
        "leaf_model": {
            "levels": ["linear_model.LinearRegression", "linear_model.PARegressor", "linear_model.Perceptron"],
            "type": "factor",
            "default": "LinearRegression",
            "core_model_parameter_type": "instance"},
            "splitter": {"levels": ["EBSTSplitter", "TEBSTSplitter", "QOSplitter"],
            "type": "factor",
            "default": "EBSTSplitter", "core_model_parameter_type": "instance()"},
        "binary_split": {
            "levels": [0, 1],
            "type": "factor",
            "default": 0,
            "core_model_parameter_type": "bool"},
        "stop_mem_management": {
            "levels": [0, 1],
            "type": "factor",
            "default": 0,
            "core_model_parameter_type": "bool"}}}
        and
        v = {'grace_period': 200,
            'max_depth': 10,
            'delta': 1e-07,
            'tau': 0.05,
            'leaf_prediction': 0,
            'leaf_model': 0,
            'model_selector_decay': 0.95,
            'splitter': 1,
            'min_samples_split': 9,
            'binary_split': 0,
            'max_size': 500.0}
        then the function returns
        {'grace_period': 200,
        'max_depth': 10,
        'delta': 1e-07,
        'tau': 0.05,
        'leaf_prediction': 'mean',
        'leaf_model': linear_model.LinearRegression,
        'model_selector_decay': 0.95,
        'splitter': 'TEBSTSplitter',
        'min_samples_split': 9,
        'binary_split': 0,
        'max_size': 500.0}.

    Args:
        fun_control (dict): dictionary with levels and types
        v (dict): dictionary with values

    Returns:
        new_dict (dict): dictionary with levels and types

    Example:
        >>> fun_control = {"HoeffdingTreeRegressor":{
                "leaf_prediction": {"levels": ["mean", "model", "adaptive"],
                                    "type": "factor",
                                    "default": "mean",
                                    "core_model_parameter_type": "str"}}}
            v = {"leaf_prediction": 0}
            get_dict_with_levels_and_types(fun_control, v)
            {"leaf_prediction": "mean"}
    """
    d = fun_control['core_model_hyper_dict']
    new_dict = {}
    for (key, value) in v.items():
        if key in d and d[key]['type'] == 'factor':
            if d[key]['core_model_parameter_type'] == 'instance':
                if 'class_name' in d[key]:
                    mdl = d[key]['class_name']
                c = d[key]['levels'][value]
                new_dict[key] = class_for_name(mdl, c)
            elif d[key]['core_model_parameter_type'] == 'instance()':
                mdl = d[key]['class_name']
                c = d[key]['levels'][value]
                k = class_for_name(mdl, c)
                new_dict[key] = k()
            else:
                new_dict[key] = d[key]['levels'][value]
        else:
            new_dict[key] = v[key]
    return new_dict

def assign_values(X: np.array, var_list: list) -> dict:
    """
    This function takes an np.array X and a list of variable names as input arguments
    and returns a dictionary where the keys are the variable names and the values are assigned from X.

    Parameters:
        X (np.array): A 2D numpy array where each column represents a variable.
        var_list (list): A list of strings representing variable names.

    Returns:
        dict: A dictionary where keys are variable names and values are assigned from X.

    Example:
        >>> import numpy as np
        >>> X = np.array([[1, 2], [3, 4], [5, 6]])
        >>> var_list = ['a', 'b']
        >>> result = assign_values(X, var_list)
        >>> print(result)
        {'a': array([1, 3, 5]), 'b': array([2, 4, 6])}
    """
    result = {}
    for (i, var_name) in enumerate(var_list):
        result[var_name] = X[:, i]
    return result

def modify_hyper_parameter_levels(fun_control, hyperparameter, levels) -> dict:
    """

    Args:
        fun_control (dict): fun_control dictionary
        hyperparameter (str): hyperparameter name
        levels (list): list of levels

    Returns:
        fun_control (dict): updated fun_control
    Example:
        >>> fun_control = {}
            core_model  = HoeffdingTreeRegressor
            fun_control.update({"core_model": core_model})
            fun_control.update({"core_model_hyper_dict": river_hyper_dict[core_model.__name__]})
            levels = ["mean", "model"]
            fun_control = modify_hyper_parameter_levels(fun_control, "leaf_prediction", levels)
    """
    fun_control['core_model_hyper_dict'][hyperparameter].update({'levels': levels})
    fun_control['core_model_hyper_dict'][hyperparameter].update({'lower': 0})
    fun_control['core_model_hyper_dict'][hyperparameter].update({'upper': len(levels) - 1})
    return fun_control

def modify_hyper_parameter_bounds(fun_control, hyperparameter, bounds) -> dict:
    """

    Args:
        fun_control (dict): fun_control dictionary
        hyperparameter (str): hyperparameter name
        bounds (list): list of two bound values. The first value represents the lower bound
            and the second value represents the upper bound.

    Returns:
        fun_control (dict): updated fun_control
    Example:
        >>> fun_control = {}
            core_model  = HoeffdingTreeRegressor
            fun_control.update({"core_model": core_model})
            fun_control.update({"core_model_hyper_dict": river_hyper_dict[core_model.__name__]})
            bounds = [3, 11]
            fun_control = modify_hyper_parameter_levels(fun_control, "min_samples_split", bounds)
    """
    fun_control['core_model_hyper_dict'][hyperparameter].update({'lower': bounds[0]})
    fun_control['core_model_hyper_dict'][hyperparameter].update({'upper': bounds[1]})
    return fun_control

def get_default_values(fun_control) -> dict:
    """Get the values from the "default" keys from the dictionary fun_control as a dict.
    If the key of the value has as "type" the value "int" or "float", convert the value to the corresponding type.
    Args:
        fun_control (dict): dictionary with levels and types
    Returns:
        new_dict (dict): dictionary with default values
    Example:
        >>> d = {"core_model_hyper_dict":{
                "leaf_prediction": {
                    "levels": ["mean", "model", "adaptive"],
                    "type": "factor",
                    "default": "mean",
                    "core_model_parameter_type": "str"},
                "leaf_model": {
                    "levels": ["linear_model.LinearRegression", "linear_model.PARegressor", "linear_model.Perceptron"],
                    "type": "factor",
                    "default": "LinearRegression",
                    "core_model_parameter_type": "instance"},
                "splitter": {
                    "levels": ["EBSTSplitter", "TEBSTSplitter", "QOSplitter"],
                    "type": "factor",
                    "default": "EBSTSplitter",
                    "core_model_parameter_type": "instance()"},
                "binary_split": {
                    "levels": [0, 1],
                    "type": "factor",
                    "default": 0,
                    "core_model_parameter_type": "bool"},
                "stop_mem_management": {
                    "levels": [0, 1],
                    "type": "factor",
                    "default": 0,
                    "core_model_parameter_type": "bool"}}}
        get_default_values_from_dict(d)
        {'leaf_prediction': 'mean',
        'leaf_model': 'linear_model.LinearRegression',
        'splitter': 'EBSTSplitter',
        'binary_split': 0,
        'stop_mem_management': 0}
    """
    d = fun_control['core_model_hyper_dict']
    new_dict = {}
    for (key, value) in d.items():
        if value['type'] == 'int':
            new_dict[key] = int(value['default'])
        elif value['type'] == 'float':
            new_dict[key] = float(value['default'])
        else:
            new_dict[key] = value['default']
    return new_dict

def get_var_type(fun_control) -> list:
    """Get the types of the values from the dictionary fun_control as a list.
    Args:
        fun_control (dict): dictionary with levels and types
    Returns:
        (list): list with types
    Example:
        >>> d = {"core_model_hyper_dict":{
            "leaf_prediction": {
                "levels": ["mean", "model", "adaptive"],
                "type": "factor",
                "default": "mean",
                "core_model_parameter_type": "str"},
            "leaf_model": {
                "levels": ["linear_model.LinearRegression", "linear_model.PARegressor", "linear_model.Perceptron"],
                "type": "factor",
                "default": "LinearRegression",
                "core_model_parameter_type": "instance"},
            "splitter": {
                "levels": ["EBSTSplitter", "TEBSTSplitter", "QOSplitter"],
                "type": "factor",
                "default": "EBSTSplitter",
                "core_model_parameter_type": "instance()"},
            "binary_split": {
                "levels": [0, 1],
                "type": "factor",
                "default": 0,
                "core_model_parameter_type": "bool"},
            "stop_mem_management": {                                                         "levels": [0, 1],
                "type": "factor",
                "default": 0,
                "core_model_parameter_type": "bool"}}}

        get_var_type(d)
        ['factor', 'factor', 'factor', 'factor', 'factor']
    """
    return list((fun_control['core_model_hyper_dict'][key]['type'] for key in fun_control['core_model_hyper_dict'].keys()))

def get_transform(fun_control) -> list:
    """Get the transformations of the values from the dictionary fun_control as a list.
    Args:
        fun_control (dict): dictionary with levels and types
    Returns:
        (list): list with transformations
    Example:
        >>> d = {"core_model_hyper_dict":{
            "leaf_prediction": {
                "levels": ["mean", "model", "adaptive"],
                "type": "factor",
                "default": "mean",
                "transform": "None",
                "core_model_parameter_type": "str"},
            "leaf_model": {
                "levels": ["linear_model.LinearRegression", "linear_model.PARegressor", "linear_model.Perceptron"],
                "type": "factor",
                "default": "LinearRegression",
                "transform": "None",
                "core_model_parameter_type": "instance"},
            "splitter": {
                "levels": ["EBSTSplitter", "TEBSTSplitter", "QOSplitter"],
                "type": "factor",
                "default": "EBSTSplitter",
                "transform": "None",
                "core_model_parameter_type": "instance()"},
            "binary_split": {
                "levels": [0, 1],
                "type": "factor",
                "default": 0,
                "transform": "None",
                "core_model_parameter_type": "bool"},
            "stop_mem_management": {                                                         "levels": [0, 1],
                "type": "factor",
                "default": 0,
                "transform": "None",
                "core_model_parameter_type": "bool"}}}

        get_transform(d)
        ['None', 'None', 'None', 'None', 'None']
    """
    return list((fun_control['core_model_hyper_dict'][key]['transform'] for key in fun_control['core_model_hyper_dict'].keys()))

def get_var_name(fun_control) -> list:
    """Get the names of the values from the dictionary fun_control as a list.
    Args:
        fun_control (dict): dictionary with names
    Returns:
        (list): list with names
    Example:
        >>> d = {"core_model_hyper_dict":{
            "leaf_prediction": {
                "levels": ["mean", "model", "adaptive"],
                "type": "factor",
                "default": "mean",
                "core_model_parameter_type": "str"},
            "leaf_model": {
                "levels": ["linear_model.LinearRegression", "linear_model.PARegressor", "linear_model.Perceptron"],
                "type": "factor",
                "default": "LinearRegression",
                "core_model_parameter_type": "instance"},
            "splitter": {
                "levels": ["EBSTSplitter", "TEBSTSplitter", "QOSplitter"],
                "type": "factor",
                "default": "EBSTSplitter",
                "core_model_parameter_type": "instance()"},
            "binary_split": {
                "levels": [0, 1],
                "type": "factor",
                "default": 0,
                "core_model_parameter_type": "bool"},
            "stop_mem_management": {                                                         "levels": [0, 1],
                "type": "factor",
                "default": 0,
                "core_model_parameter_type": "bool"}}}

        get_var_name(d)
        ['leaf_prediction', 'leaf_model', 'splitter', 'binary_split', 'stop_mem_management']
    """
    return list(fun_control['core_model_hyper_dict'].keys())

def get_bound_values(fun_control: dict, bound: str, as_list=False) -> list or np.array:
    """Generate a list from a dictionary.
    It takes the values from the keys "bound" in the
    fun_control[]"core_model_hyper_dict"] dictionary and
    returns a list of the values in the same order as the keys in the
    dictionary.
    For example if the dictionary is
    {"a": {"upper": 1}, "b": {"upper": 2}}
    the list is [1, 2] if bound="upper".
    Args:
        fun_control (dict): dictionary with upper values
        bound (str): either "upper" or "lower"
    Returns:
        (list): list with lower or upper values
    """
    if bound not in ['upper', 'lower']:
        raise ValueError("bound must be either 'upper' or 'lower'")
    d = fun_control['core_model_hyper_dict']
    b = []
    for (key, value) in d.items():
        b.append(value[bound])
    if as_list:
        return b
    else:
        return np.array(b)

def replace_levels_with_positions(hyper_dict, hyper_dict_values) -> dict:
    """Replace the levels with the position in the levels list.
    The function that takes two dictionaries.
    The first contains as hyperparameters as keys.
    If the hyperparameter has the key "levels",
    then the value of the corresponding hyperparameter in the second dictionary is
    replaced by the position of the value in the list of levels.
    The function returns a dictionary with the same keys as the second dictionary.
    For example, if the second dictionary is {"a": 1, "b": "model1", "c": 3}
    and the first dictionary is {
        "a": {"type": "int"},
        "b": {"levels": ["model4", "model5", "model1"]},
        "d": {"type": "float"}},
    then the function should return {"a": 1, "b": 2, "c": 3}.
    Args:
        hyper_dict (dict): dictionary with levels
        hyper_dict_values (dict): dictionary with values
    Returns:
        (dict): dictionary with values
    Example:
        >>> hyper_dict = {"leaf_prediction": {
        "levels": ["mean", "model", "adaptive"],
        "type": "factor",
        "default": "mean",
        "core_model_parameter_type": "str"},
        "leaf_model": {
            "levels": ["linear_model.LinearRegression", "linear_model.PARegressor", "linear_model.Perceptron"],
            "type": "factor",
            "default": "LinearRegression",
            "core_model_parameter_type": "instance"},
        "splitter": {
            "levels": ["EBSTSplitter", "TEBSTSplitter", "QOSplitter"],
            "type": "factor",
            "default": "EBSTSplitter",
            "core_model_parameter_type": "instance()"},
        "binary_split": {
            "levels": [0, 1],
            "type": "factor",
            "default": 0,
            "core_model_parameter_type": "bool"},
        "stop_mem_management": {
            "levels": [0, 1],
            "type": "factor",
            "default": 0,
            "core_model_parameter_type": "bool"}}
        >>> hyper_dict_values = {"leaf_prediction": "mean",
        "leaf_model": "linear_model.LinearRegression",
        "splitter": "EBSTSplitter",
        "binary_split": 0,
        "stop_mem_management": 0}
        >>> replace_levels_with_position(hyper_dict, hyper_dict_values)
        {'leaf_prediction': 0,
        'leaf_model': 0,
        'splitter': 0,
        'binary_split': 0,
        'stop_mem_management': 0}
    """
    hyper_dict_values_new = copy.deepcopy(hyper_dict_values)
    for (key, value) in hyper_dict_values.items():
        if key in hyper_dict.keys():
            if 'levels' in hyper_dict[key].keys():
                hyper_dict_values_new[key] = hyper_dict[key]['levels'].index(value)
    return hyper_dict_values_new

def get_values_from_dict(dictionary) -> np.array:
    """Get the values from a dictionary as an array.
    Generate an np.array that contains the values of the keys of a dictionary
    in the same order as the keys of the dictionary.
    Args:
        dictionary (dict): dictionary with values
    Returns:
        (np.array): array with values
    Example:
        >>> d = {"a": 1, "b": 2, "c": 3}
        >>> get_values_from_dict(d)
        array([1, 2, 3])
    """
    return np.array(list(dictionary.values()))

def add_core_model_to_fun_control(core_model, fun_control, hyper_dict, filename) -> dict:
    """Add the core model to the function control dictionary.
    Args:
        core_model (class): The core model.
        fun_control (dict): The function control dictionary.
        hyper_dict (dict): The hyper parameter dictionary.
        filename (str): The name of the json file that contains the hyper parameter dictionary.
        Optional. Default is None.
    Returns:
        (dict): The function control dictionary.
    Example:
        >>> from river.tree import HoeffdingAdaptiveTreeRegressor
            from spotRiver.data.river_hyper_dict import RiverHyperDict
            fun_control = {}
            add_core_model_to_fun_control(core_model=HoeffdingAdaptiveTreeRegressor,
                fun_control=func_control,
                hyper_dict=RiverHyperDict,
                filename=None)
    """
    fun_control.update({'core_model': core_model})
    if filename is None:
        new_hyper_dict = hyper_dict().load()
    else:
        with open('river_hyper_dict.json', 'r') as f:
            new_hyper_dict = json.load(f)
    hyper_dict().load()
    fun_control.update({'core_model_hyper_dict': new_hyper_dict[core_model.__name__]})
    return fun_control

def get_one_core_model_from_X(X, fun_control=None):
    var_dict = assign_values(X, fun_control['var_name'])
    config = return_conf_list_from_var_dict(var_dict, fun_control)[0]
    core_model = fun_control['core_model'](**config)
    return core_model

def get_one_sklearn_model_from_X(X, fun_control=None):
    core_model = get_one_core_model_from_X(X=X, fun_control=fun_control)
    if fun_control['prep_model'] is not None:
        model = make_pipeline(fun_control['prep_model'], core_model)
    else:
        model = core_model
    return model

def get_one_river_model_from_X(X, fun_control=None):
    core_model = get_one_core_model_from_X(X=X, fun_control=fun_control)
    if fun_control['prep_model'] is not None:
        model = compose.Pipeline(fun_control['prep_model'], core_model)
    else:
        model = core_model
    return model

def get_default_hyperparameters_as_array(fun_control, hyper_dict) -> np.array:
    X0 = get_default_values(fun_control)
    X0 = replace_levels_with_positions(hyper_dict[fun_control['core_model'].__name__], X0)
    X0 = get_values_from_dict(X0)
    X0 = np.array([X0])
    X0.shape[1]
    return X0

def get_default_hyperparameters_for_core_model(fun_control) -> dict:
    values = get_default_values(fun_control)
    values = get_dict_with_levels_and_types(fun_control=fun_control, v=values)
    values = convert_keys(values, fun_control['var_type'])
    values = transform_hyper_parameter_values(fun_control=fun_control, hyper_parameter_values=values)
    return values