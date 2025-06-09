from typing import List, TYPE_CHECKING, Tuple, Any, Optional
from ..parser.SystemRDLParser import SystemRDLParser
from .BaseVisitor import BaseVisitor
from .ExprVisitor import ExprVisitor
from .helpers import get_ID_text
from . import helpers
from ..ast import AssignmentCast
from ..source_ref import src_ref_from_antlr
from .. import rdltypes
if TYPE_CHECKING:
    from antlr4.Token import CommonToken
    from ..source_ref import SourceRefBase
    from ..compiler import RDLCompiler
    from .. import component as comp
    from typing import Type

class EnumVisitor(BaseVisitor):

    def __init__(self, compiler: 'RDLCompiler', parent_component: 'comp.Component') -> None:
        super().__init__(compiler)
        self.parent_component = parent_component

    def visitEnum_def(self, ctx):
        self.compiler.namespace.enter_scope()
        self.compiler.namespace.parent_parameters_visible = False
        enum_name = get_ID_text(ctx.ID())
        entry_values = []
        entry_names = []
        members = []
        for enum_entry_ctx in ctx.getTypedRuleContexts(SystemRDLParser.Enum_entryContext):
            name_token, value_expr_ctx, rdl_name, rdl_desc = self.visit(enum_entry_ctx)
            entry_name = get_ID_text(name_token)
            if entry_name in entry_names:
                self.msg.fatal("Entry '%s' has already been defined in this enum" % entry_name, src_ref_from_antlr(name_token))
            entry_names.append(entry_name)
            if value_expr_ctx is not None:
                visitor = ExprVisitor(self.compiler)
                expr = visitor.visit(value_expr_ctx)
                expr = AssignmentCast(self.compiler.env, value_expr_ctx, expr, int)
                expr.predict_type()
                entry_value = expr.get_value()
            elif not entry_values:
                entry_value = 0
            else:
                entry_value = entry_values[-1] + 1
            if entry_value in entry_values:
                self.msg.fatal('Enumeration encoding values must be unique', src_ref_from_antlr(name_token))
            entry_values.append(entry_value)
            members.append(rdltypes.UserEnumMemberContainer(entry_name, entry_value, rdl_name, rdl_desc))
        enum_type = rdltypes.UserEnum.define_new(enum_name, members, self.parent_component)
        self.compiler.namespace.exit_scope()
        self.compiler.namespace.parent_parameters_visible = True
        return (enum_type, get_ID_text(ctx.ID()), src_ref_from_antlr(ctx.ID()))

    def visitEnum_entry(self, ctx: SystemRDLParser.Enum_entryContext) -> Tuple['CommonToken', SystemRDLParser.ExprContext, Optional[str], Optional[str]]:
        name_token = ctx.ID()
        value_expr_ctx = ctx.expr()
        rdl_name = None
        rdl_desc = None
        for pa_ctx in ctx.getTypedRuleContexts(SystemRDLParser.Enum_prop_assignContext):
            prop_token, prop_value = self.visit(pa_ctx)
            prop_name = get_ID_text(prop_token)
            if prop_name == 'desc':
                if rdl_desc is not None:
                    self.msg.error("Property 'desc' was already assigned in this scope", src_ref_from_antlr(prop_token))
                    continue
                if self.compiler.env.dedent_desc:
                    rdl_desc = helpers.dedent_text(prop_value)
                else:
                    rdl_desc = prop_value
            elif prop_name == 'name':
                if rdl_name is not None:
                    self.msg.error("Property 'name' was already assigned in this scope", src_ref_from_antlr(prop_token))
                    continue
                rdl_name = prop_value
            else:
                self.msg.fatal("Illegal enum property assignment '%s'" % prop_name, src_ref_from_antlr(prop_token))
        return (name_token, value_expr_ctx, rdl_name, rdl_desc)

    def visitEnum_prop_assign(self, ctx: SystemRDLParser.Enum_prop_assignContext) -> Tuple['CommonToken', Any]:
        prop_token = ctx.ID()
        visitor = ExprVisitor(self.compiler)
        prop_expr = visitor.visit(ctx.expr())
        prop_expr = AssignmentCast(self.compiler.env, ctx.expr(), prop_expr, str)
        prop_expr.predict_type()
        prop_value = prop_expr.get_value()
        return (prop_token, prop_value)