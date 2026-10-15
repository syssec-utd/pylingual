import ast
import sys
import re
import copy
from pylingual.masking.global_masker import Masker
from pylingual.utils.version import PythonVersion

_RUNTIME_PYTHON_VERSION = PythonVersion(sys.version_info)

if _RUNTIME_PYTHON_VERSION >= (3, 14):
    from _ast_unparse import Unparser, _Precedence
else:
    Unparser = ast._Unparser
    _Precedence = ast._Precedence


class customUnparser(Unparser):
    def __init__(self, masker: Masker, **kwargs):
        Unparser.__init__(self, **kwargs)
        self.masker = masker

    def visit_Constant(self, node):
        value = node.value
        if isinstance(value, tuple):
            with self.delimit("(", ")"):
                self.items_view(self._write_constant, value)
        elif value is ...:
            self.write("...")
        else:
            if value in self.masker.global_tab.values():
                # get key from value in dictionary
                key = self.masker.unmask(value)
                if not isinstance(key, str):
                    self.write(value)
                    return
            self._write_constant(value)

    def visit_FormattedValue(self, node):
        def unparse_inner(inner):
            if _RUNTIME_PYTHON_VERSION <= (3, 11):
                unparser = type(self)(self.masker, _avoid_backslashes=True)
            else:
                unparser = type(self)(self.masker)
            unparser.set_precedence(_Precedence.TEST.next(), inner)
            return unparser.visit(inner)

        with self.delimit("{", "}"):
            expr = unparse_inner(node.value)
            if "\\" in expr:
                raise ValueError("Unable to avoid backslash in f-string expression part")
            if expr.startswith("{"):
                # Separate pair of opening brackets as "{ {"
                self.write(" ")
            self.write(expr)
            if node.conversion != -1:
                self.write(f"!{chr(node.conversion)}")
            if node.format_spec:
                self.write(":")
                if _RUNTIME_PYTHON_VERSION >= (3, 14):
                    self._write_ftstring_inner(node.format_spec, is_format_spec=True)
                else:
                    self._write_fstring_inner(node.format_spec)


def custom_unparse(ast_obj, masker: Masker):
    unparser = customUnparser(masker)
    return unparser.visit(ast_obj)


def evaluate_binop_optimizations(node: ast.BinOp, version):
    def eval_expr_binop(binop):
        if ast.BinOp in (type(binop.left), type(binop.right)):
            if type(binop.left) == ast.BinOp:
                binop.left = eval_expr_binop(binop.left)
            if type(binop.right) == ast.BinOp:
                binop.right = eval_expr_binop(binop.right)

        if ast.UnaryOp in (type(binop.left), type(binop.right)):
            if type(binop.left) == ast.UnaryOp:
                binop.left = evaluate_unaryop_optimizations(binop.left, version)
            if type(binop.right) == ast.UnaryOp:
                binop.right = evaluate_unaryop_optimizations(binop.right, version)

        if type(binop.left) == type(binop.right) == ast.Constant:
            # don't simplify if the calculation throws an error
            try:
                value = eval(compile(ast.fix_missing_locations(ast.Expression(binop)), "", "eval"))
            except (TypeError, ZeroDivisionError):
                return binop
            # following two checks are for catching cases where the compiler will not premptively evaluate the expression
            # see max sizes in cpython: https://github.com/python/cpython/blob/34e93d3998bab8acd651c50724eb1977f4860a08/Python/ast_opt.c#LL156C1-L156C1
            if type(value) in (str, bytes):
                if len(value) > 20 and version == (3, 6) and type(binop.op) == ast.Mult:
                    return binop
                if len(value) > 4096:
                    return binop
            elif type(value) == int:
                if len(bin(value)[2:]) > 128:
                    return binop

            # % style string formatting is not optimized by the compiler
            if type(binop.left.value) == str and type(binop.right.value) == str and type(binop.op) == ast.Mod:
                return binop
            return ast.Constant(value=value)

        return binop

    return eval_expr_binop(node)


def evaluate_unaryop_optimizations(node: ast.UnaryOp, version):
    def eval_expr_unaryop(unaryop: ast.UnaryOp):
        if type(unaryop.operand) == ast.UnaryOp:
            unaryop.operand = eval_expr_unaryop(unaryop.operand)

        if type(unaryop.operand) == ast.BinOp:
            unaryop.operand = evaluate_binop_optimizations(unaryop.operand, version)

        if type(unaryop.operand) == ast.Constant:
            # don't simplify if the calculation throws an error
            try:
                value = eval(ast.unparse(unaryop))
            except TypeError:
                return unaryop
            return ast.Constant(value=value)

        return unaryop

    return eval_expr_unaryop(node)


class RewriteMasks(ast.NodeTransformer):
    def __init__(self, masker: Masker, line_offsets: dict, python_version: PythonVersion):
        self.masker = masker
        self.line_offsets = line_offsets
        self.python_version = python_version

    def visit_Name(self, node):
        if node.id in self.masker.global_tab:
            node.id = self.masker.mask(node.id)

        self.generic_visit(node)
        return node

    def visit_Constant(self, node):
        """Replace constants as well as calculate line_offsets introduced by replacing multiline strings"""
        # update lno for multiline
        if node.value in self.masker.global_tab:
            if hasattr(node, "lineno") and hasattr(node, "end_lineno"):
                if node.end_lineno > node.lineno:
                    self.line_offsets.update({node.lineno: node.end_lineno - node.lineno})

            node.value = self.masker.mask(node.value)
        self.generic_visit(node)
        return node

    def visit_Global(self, node):
        # drop unused globals; mask all others
        node.names = [self.masker.mask(name) for name in node.names if name in self.masker.global_tab]
        self.generic_visit(node)
        return node

    def visit_Nonlocal(self, node):
        node.names = [self.masker.mask(name) for name in node.names]
        self.generic_visit(node)
        return node

    def visit_BinOp(self, node):
        node = evaluate_binop_optimizations(node, self.masker.version)

        if isinstance(node, ast.Constant):
            node = self.visit_Constant(node)
        elif isinstance(node, ast.Name):
            node = self.visit_Name(node)

        self.generic_visit(node)

        # handle printf-style string formatting in 3.11
        if isinstance(node, ast.BinOp) and self.python_version >= (3, 11):
            if isinstance(node.op, ast.Mod) and isinstance(node.left, ast.Constant) and isinstance(node.left.value, str) and type(node.right) in (ast.Tuple, ast.List):
                format_specifier_re = r"(%[\#0\- \+]*(?:\*|\d+)?(?:.(?:\*|\d+))?[diouxXeEfFgGcrsa%])"
                string_fragments = re.split(format_specifier_re, node.left.value)

                # resolve "%%" -> "%"; this isn't a real format specifier
                for i in range(1, len(string_fragments) - 1, 2):
                    while string_fragments[i] == "%%":
                        string_fragments[i - 1] += "%" + string_fragments[i + 1]
                        string_fragments[i - 1 :] = string_fragments[i + 1 :]
                # mask each fragment individually
                if len(string_fragments) > 1:
                    for i, fragment in enumerate(string_fragments):
                        # don't try to mask the format specifier
                        if i % 2 == 1 or not fragment:
                            continue
                        string_fragments[i] = self.masker.mask(fragment)
                    node.left.value = "".join(string_fragments)

        return node

    def visit_UnaryOp(self, node):
        # simplify negative numbers
        node = evaluate_unaryop_optimizations(node, self.masker.version)

        if isinstance(node, ast.Constant):
            node = self.visit_Constant(node)
        elif isinstance(node, ast.Name):
            node = self.visit_Name(node)

        self.generic_visit(node)
        return node

    def visit_FunctionDef(self, node):
        node.name = self.masker.mask(node.name)

        if node.returns is not None and ast.unparse(node.returns) in self.masker.global_tab:
            node.returns = ast.Name(id=ast.unparse(node.returns))

        self.generic_visit(node)
        return node

    def visit_AsyncFunctionDef(self, node):
        # mask return annotation
        node.name = self.masker.mask(node.name)

        if node.returns is not None and ast.unparse(node.returns) in self.masker.global_tab:
            node.returns = ast.Name(id=ast.unparse(node.returns))

        self.generic_visit(node)
        return node

    def visit_ClassDef(self, node):
        node.name = self.masker.mask(node.name)
        self.generic_visit(node)
        return node

    def visit_Attribute(self, node):
        if node.attr in self.masker.global_tab:
            node.attr = self.masker.mask(node.attr)
        elif ast.unparse(node) in self.masker.global_tab:
            node = ast.Name(id=self.masker.mask(ast.unparse(node)))
        self.generic_visit(node)
        return node

    def visit_AnnAssign(self, node):
        if self.masker.future_annotations:
            if ast.unparse(node.annotation) in self.masker.global_tab:
                node.annotation = ast.Name(id=self.masker.mask(ast.unparse(node.annotation)))
            elif node.value is not None:
                # if we can't mask the annotation, just remove the annotation
                node = ast.Assign(targets=[node.target], value=node.value, lineno=node.lineno)
            self.generic_visit(node)
        else:
            self.generic_visit(node)
            if node.value is not None and not re.match(r'["\'(\[]*<', ast.unparse(node.annotation)):
                # if we can't mask the annotation, just remove the annotation
                node = ast.Assign(targets=[node.target], value=node.value, lineno=node.lineno)
        return node

    def visit_ImportFrom(self, node):
        if node.module is None:  # edge case for "from .. import func"
            node.module = self.masker.mask("")
        else:
            node.module = self.masker.mask(node.module)
        node.module = str(self.masker.mask(node.level)) + str(node.module or "")
        node.level = 0
        self.generic_visit(node)
        return node

    def visit_arg(self, node):
        node.arg = self.masker.mask(node.arg)

        if node.annotation and ast.unparse(node.annotation) in self.masker.global_tab:
            node.annotation = ast.Name(id=ast.unparse(node.annotation))

        self.generic_visit(node)
        return node

    def visit_alias(self, node):
        if node.name not in "*":
            node.name = self.masker.mask(node.name)
        if node.asname is not None:
            node.asname = self.masker.global_tab.get(node.asname, node.asname)
        self.generic_visit(node)
        return node

    def visit_keyword(self, node):
        if node.arg is not None:
            node.arg = self.masker.mask(node.arg)
        self.generic_visit(node)
        return node

    def visit_ExceptHandler(self, node):
        if getattr(node, "name", None) is not None:
            node.name = self.masker.mask(node.name)
        self.generic_visit(node)
        return node

    def visit_If(self, node):
        # don't try to mask trivially unreachable code
        if isinstance(node.test, ast.Constant):
            # we have to use deepcopy due to how generic_visit masks nodes, we cannot pass it the individual body.
            if node.test.value is False:
                # only mask else body
                masked_node = copy.deepcopy(node)
                self.generic_visit(masked_node)
                node.orelse = copy.deepcopy(masked_node.orelse)
                return node
            if node.test.value is True:
                # only mask if body
                masked_node = copy.deepcopy(node)
                self.generic_visit(masked_node)
                node.body = copy.deepcopy(masked_node.body)
                return node

        self.generic_visit(node)
        return node


DUMMY_DECORATOR = "PYLINGUAL_DUMMY_DECORATOR_finj3igh309jhasfjn2oihg20ni3"


def add_dummy_decorators(source: str) -> str:
    tree = ast.parse(source)
    dummy_deco_transformer().generic_visit(tree)
    return ast.unparse(tree)


class dummy_deco_transformer(ast.NodeTransformer):
    def visit_ClassDef(self, node):
        node.decorator_list.append(ast.Name(id=DUMMY_DECORATOR))
        self.generic_visit(node)
        return node

    def visit_AsyncFunctionDef(self, node):
        node.decorator_list.append(ast.Name(id=DUMMY_DECORATOR))
        self.generic_visit(node)
        return node

    def visit_FunctionDef(self, node):
        node.decorator_list.append(ast.Name(id=DUMMY_DECORATOR))
        self.generic_visit(node)
        return node
