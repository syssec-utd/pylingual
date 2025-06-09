from typing import cast
from xformula.runtime.core.context.abc import RuntimeContext
from xformula.syntax.ast.nodes.abc import SimpleExpression
from xformula.syntax.core.features.containers.ast.nodes import Tuple as TupleNode
from xformula.syntax.grammar.ebnf import non_terminal
from xformula.syntax.grammar.non_terminals.abc import NonTerminal
from xformula.syntax.parser.trees.abc import ParseTree
__all__ = ['Tuple']

class Tuple(NonTerminal[TupleNode]):

    class Meta:
        atomic = True
        tags = {non_terminal('Primary'): 4000}

    def build_grammar(self) -> str:
        suite = self.ebnf.suite
        define = self.ebnf.define
        orelse = self.ebnf.orelse
        use_template = self.ebnf.use_template
        op = self.ebnf.op
        _non_terminal = self.ebnf.non_terminal
        optional = self.ebnf.optional
        return suite(define(op('('), use_template('SeparatedOneOrMoreOf', op(','), _non_terminal('SimpleExpression')), optional(op(',')), op(')')), orelse(op('('), _non_terminal('SimpleExpression'), op(','), op(')')), orelse(op('('), op(')')))

    def transform_parse_tree(self, runtime_context: RuntimeContext, tree: ParseTree[SimpleExpression]) -> TupleNode:
        return TupleNode(elements=cast(list[SimpleExpression], tree.children))