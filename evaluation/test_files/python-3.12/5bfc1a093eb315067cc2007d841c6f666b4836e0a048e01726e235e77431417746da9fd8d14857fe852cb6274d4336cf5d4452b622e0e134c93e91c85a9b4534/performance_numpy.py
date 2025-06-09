from __future__ import annotations
import ast
from typing import Callable
from pyrefact import parsing, processing

def uses_numpy(root: ast.Module) -> bool:
    if 'numpy' in parsing.module_dependencies(root):
        return True
    return any(parsing.walk(root, ast.Attribute(value=ast.Name(id=('numpy', 'np')))))

def _only_if_uses_numpy(f: Callable) -> Callable:

    def wrapper(source: str) -> str:
        root = parsing.parse(source)
        if not uses_numpy(root):
            return source
        return f(source)
    return wrapper

def _is_sum_call(call: ast.Call):
    return parsing.is_call(call, ('sum', 'np.sum', 'numpy.sum'))

def _is_np_array_call(call: ast.Call) -> bool:
    return parsing.is_call(call, ('np.array', 'numpy.array'))

def _is_zip_product(comp: ast.ListComp | ast.GeneratorExp):
    elt_template = ast.BinOp(op=ast.Mult, left=ast.Name, right=ast.Name)
    generator_template = ast.comprehension(ifs=[], target=ast.Tuple(elts=[ast.Name, ast.Name]), iter=ast.Call(func=ast.Name(id='zip')))
    return parsing.match_template(comp.elt, elt_template) and parsing.match_template(comp.generators, [generator_template]) and ({x.id for x in comp.generators[0].target.elts} == {comp.elt.left.id, comp.elt.right.id})

def _wrap_np_dot(*args: ast.AST) -> ast.Call:
    return ast.Call(func=ast.Attribute(value=ast.Name(id='np'), attr='dot'), args=list(args), keywords=[])

def _wrap_np_matmul(*args: ast.AST) -> ast.Call:
    return ast.Call(func=ast.Attribute(value=ast.Name(id='np'), attr='matmul'), args=list(args), keywords=[])

def wrap_transpose(node: ast.AST) -> ast.Attribute:
    return ast.Attribute(value=node, attr='T')

@processing.fix
def simplify_matmul_transposes(source: str) -> str:
    """Replace np.matmul(a.T, b.T).T with np.matmul(b, a), if found."""
    root = parsing.parse(source)
    target_template = ast.Call(func=ast.Attribute(value=ast.Name(id=('np', 'numpy')), attr='matmul'), args=[object, object])
    for node in filter(parsing.is_transpose_operation, parsing.walk(root, ast.Attribute)):
        target = parsing.transpose_target(node)
        if parsing.match_template(target, target_template) and (not any((isinstance(arg, ast.Starred) for arg in target.args))) and all((parsing.is_transpose_operation(arg) for arg in target.args)):
            left, right = target.args
            matmul = _wrap_np_matmul(wrap_transpose(right), wrap_transpose(left))
            matmul.func = target.func
            matmul.keywords = target.keywords
            yield (node, matmul)

@_only_if_uses_numpy
@processing.fix
def replace_implicit_dot(source: str) -> str:
    root = parsing.parse(source)
    template = ast.Call(args=[(ast.ListComp, ast.GeneratorExp)], keywords=[])
    for call in parsing.walk(root, template):
        if _is_sum_call(call) and _is_zip_product(call.args[0]):
            zip_args = call.args[0].generators[0].iter.args
            yield (call, _wrap_np_dot(*zip_args))

@_only_if_uses_numpy
@processing.fix
def replace_implicit_matmul(source: str) -> str:
    root = parsing.parse(source)
    comp_template = ast.ListComp(generators=[ast.comprehension(ifs=[], target=ast.Name, iter=(ast.Name, ast.Attribute(attr='T')))])
    template = ast.Call(args=[ast.ListComp(elt=ast.ListComp)], keywords=[])
    for call in filter(_is_np_array_call, parsing.walk(root, template)):
        comp_outer = call.args[0]
        comp_inner = comp_outer.elt
        if parsing.match_template(comp_outer, comp_template) and parsing.match_template(comp_inner, comp_template):
            if parsing.is_call(comp_inner.elt, ('numpy.dot', 'np.dot')):
                left_id = comp_inner.generators[0].target.id if isinstance(comp_inner.generators[0].target, ast.Name) else comp_inner.generators[0].target.value.id
                right_id = comp_outer.generators[0].target.id if isinstance(comp_outer.generators[0].target, ast.Name) else comp_outer.generators[0].target.value.id
                if (comp_inner.generators[0].target.id, comp_outer.generators[0].target.id) in ((left_id, right_id), (right_id, left_id)):
                    yield (call, wrap_transpose(_wrap_np_matmul(comp_inner.generators[0].iter, wrap_transpose(comp_outer.generators[0].iter))))