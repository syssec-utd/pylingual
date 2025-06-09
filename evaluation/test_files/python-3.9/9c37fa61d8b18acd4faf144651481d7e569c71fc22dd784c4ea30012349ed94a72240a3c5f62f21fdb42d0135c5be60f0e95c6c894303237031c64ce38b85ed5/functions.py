from typing import Callable, Mapping, Tuple, Sequence, Union
from .datastructures import WorkflowContext
from .exceptions import WorkflowSetupError

def extract_inputs(func: Callable) -> Tuple[Mapping[str, type], str]:
    """
    Extract input variables from function
    """
    func_code = func.__code__
    annotations = func.__annotations__
    if func_code.co_posonlyargcount:
        raise WorkflowSetupError(f'Positional only arguments are not supported.\n\n\tdef {func_code.co_name}(...)')
    inputs = {}
    context_var = None
    total_args = sum((getattr(func_code, name, 0) for name in ('co_argcount', 'co_posonlyargcount', 'co_kwonlyargcount')))
    for name in func_code.co_varnames[:total_args]:
        type_ = annotations.get(name)
        if type_ is WorkflowContext:
            if context_var is not None:
                raise WorkflowSetupError(f'WorkflowContext supplied multiple times.\n\n\tdef {func_code.co_name}({context_var}: WorkflowContext, {name}: WorkflowContext)')
            context_var = name
        else:
            inputs[name] = type_
    return (inputs, context_var)

def extract_outputs(func: Callable, names: Union[str, Sequence[str]]) -> Sequence[Tuple[str, type]]:
    """
    Extract outputs from function
    """
    types = func.__annotations__.get('return')
    if names is None:
        names = ()
    if isinstance(names, str):
        names = (names,)
    if types is None:
        types = ()
    elif getattr(types, '_name', None) == 'Tuple':
        types = types.__args__
    else:
        types = (types,)
    if len(names) != len(types):
        raise WorkflowSetupError('Name count does not match type count.')
    return tuple(zip(names, types))

def call_nodes(context: WorkflowContext, nodes: Sequence[Callable]):
    """
    Call each node in a sequence
    """
    for node in nodes:
        node(context)