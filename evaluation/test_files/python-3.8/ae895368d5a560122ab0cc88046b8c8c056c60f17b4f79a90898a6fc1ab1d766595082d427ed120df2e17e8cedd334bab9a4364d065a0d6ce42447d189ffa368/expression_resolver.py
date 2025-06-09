"""
This module makes it possible to parse expressions including all their subexpressions, if present.
for example ahb_expressions which contain condition_expressions or condition_expressions which contain packages.
Parsing expressions that are nested into other expressions is referred to as "resolving".
"""
import asyncio
import inspect
from typing import Awaitable, List, Optional, Union
import inject
from lark import Token, Transformer, Tree
from lark.exceptions import VisitError
from ahbicht.content_evaluation.evaluationdatatypes import EvaluatableData, EvaluatableDataProvider
from ahbicht.content_evaluation.token_logic_provider import TokenLogicProvider
from ahbicht.expressions.ahb_expression_parser import parse_ahb_expression_to_single_requirement_indicator_expressions
from ahbicht.expressions.condition_expression_parser import parse_condition_expression_to_tree
from ahbicht.expressions.package_expansion import PackageResolver
from ahbicht.mapping_results import Repeatability, parse_repeatability

async def parse_expression_including_unresolved_subexpressions(expression: str, resolve_packages: bool=False, replace_time_conditions: bool=True) -> Tree[Token]:
    """
    Parses expressions and resolves its subexpressions,
    for example condition_expressions in ahb_expressions or packages in condition_expressions.
    :param expression: a syntactically valid ahb_expression or condition_expression
    :param resolve_packages: if true resolves also the packages in the condition_expressions
    :param replace_time_conditions: if true the time conditions "UBx" are replaced with format constraints
    """
    try:
        expression_tree = parse_ahb_expression_to_single_requirement_indicator_expressions(expression)
        expression_tree = AhbExpressionResolverTransformer().transform(expression_tree)
    except SyntaxError as ahb_syntax_error:
        try:
            expression_tree = parse_condition_expression_to_tree(expression)
        except SyntaxError as condition_syntax_error:
            raise SyntaxError(f'{ahb_syntax_error.msg} {condition_syntax_error.msg}')
    if resolve_packages:
        expression_tree = await expand_packages(expression_tree)
    if replace_time_conditions:
        expression_tree = expand_time_conditions(expression_tree)
    return expression_tree

async def expand_packages(parsed_tree: Tree) -> Tree[Token]:
    """
    Replaces all the "short" packages in parser_tree with the respective "long" condition expressions
    """
    try:
        result = PackageExpansionTransformer().transform(parsed_tree)
    except VisitError as visit_err:
        raise visit_err.orig_exc
    result = await _replace_sub_coroutines_with_awaited_results(result)
    return result

def expand_time_conditions(parsed_tree: Tree) -> Tree[Token]:
    """
    Replaces all the time conditions "UBx" with format constraints (and requirements constraints for UB3)
    """
    result = TimeConditionTransformer().transform(parsed_tree)
    return result

async def _replace_sub_coroutines_with_awaited_results(tree: Union[Tree, Awaitable[Tree]]) -> Tree[Token]:
    """
    awaits all coroutines inside the tree and replaces the coroutines with their respective awaited result.
    returns an updated tree
    """
    result: Tree
    if inspect.isawaitable(tree):
        result = await tree
    else:
        result = tree
    sub_results = await asyncio.gather(*result.scan_values(asyncio.iscoroutine))
    for (coro, sub_result) in zip(result.scan_values(asyncio.iscoroutine), sub_results):
        for sub_tree in result.iter_subtrees():
            for (child_index, child) in enumerate(sub_tree.children):
                if child == coro:
                    sub_tree.children[child_index] = sub_result
    return result

class AhbExpressionResolverTransformer(Transformer):
    """
    Resolves the condition_expressions inside an ahb_expression.
    """

    def CONDITION_EXPRESSION(self, expression):
        """
        Replacing the expression_condition with its parsed tree.
        """
        condition_tree = parse_condition_expression_to_tree(expression.value)
        return condition_tree

class PackageExpansionTransformer(Transformer):
    """
    The PackageExpansionTransformer expands packages inside a tree to condition expressions by using a PackageResolver.
    """

    def __init__(self):
        super().__init__()
        self.token_logic_provider: TokenLogicProvider = inject.instance(TokenLogicProvider)

    def package(self, tokens: List[Token]) -> Awaitable[Tree]:
        """
        try to resolve the package using the injected PackageResolver
        """
        package_key_token = [t for t in tokens if t.type == 'PACKAGE_KEY'][0]
        repeatability_tokens = [t for t in tokens if t.type == 'REPEATABILITY']
        repeatability: Optional[Repeatability]
        if len(repeatability_tokens) == 1:
            repeatability = parse_repeatability(repeatability_tokens[0].value)
        else:
            repeatability = None
        return self._package_async(package_key_token)

    @inject.params(evaluatable_data=EvaluatableDataProvider)
    async def _package_async(self, package_key_token: Token, evaluatable_data: EvaluatableData) -> Tree[Token]:
        resolver: PackageResolver = self.token_logic_provider.get_package_resolver(evaluatable_data.edifact_format, evaluatable_data.edifact_format_version)
        resolved_package = await resolver.get_condition_expression(package_key_token.value)
        if not resolved_package.has_been_resolved_successfully():
            raise NotImplementedError(f"The package '{package_key_token.value}' could not be resolved by {resolver}")
        tree_result = parse_condition_expression_to_tree(resolved_package.package_expression)
        return tree_result

class TimeConditionTransformer(Transformer):
    """
    The TimeConditionEvaluator replaces "time conditions" (aka "UB1", "UB2", "UB3") with evaluatable format constraints.
    This is not what BDEW suggests us to do in the "Allgemeine Festlegungen". BDEW says that "UBx" conditions have to be
    expanded just like packages: For example "UB1" shall be expanded to "([931] ∧ [932] [490]) ⊻ ([931] ∧ [933] [491])".

    This just doesn't work out for multiple reasons:

    1. Other than _all_ the other requirement constraints RC 490, 491, 492 and 493 are self-referencing.
    While "normal" RCs act like "You have to provide this ("Foo") if the other thing ("Bar") meets a requirement",
    the 49x RCs are of kind "This ("Foo") has to meet certain requirements (e.g. the end of a German day), regardless
    of the other things ("Bar"). So the usual requirement constraint evaluation approach ("Search for Bar and derive
    from there what it means for this (Foo)") won't work and is overly complicated, too.
    Also, if the pseudo requirement constraint 490-493 is UNFULFILLED, this does _not_ mean that the data must not
    be provided which is also a different behaviour compared to usual requirement constraints.

    2. No one who understands the concept of datetime+offset and is able to parse datetime+offset nowadays cares, if you
    use ("x datetime" with an "0 offset") or ("x+z datetime" that has a "z offset") instead. It's just BDEWs home-brewed
    EDIFACT serialization rule that, for no real reason, restricts us to set the offset z to "+00:00" always.
    https://imgflip.com/i/65giq5

    AHBicht won't restrict you to use datetime offset=="+00:00". Because we don't care and you should not care.
    The scope of AHBicht is to evaluate expressions and data, not to obey pointless BDEW EDIFACT rules.
    Also this default transformer won't expand the UBx conditions into something which is overly complicated and in the
    end does really fit (for above reasons).

    That being said… the thing that actually happens is:
    UBx will be replaced with a format constraint (plus a requirement constraint in case of UB3) that is fulfilled,
    if and only if the value provided obeys the original *meaning* of UBx.
    So the data provided will be evaluated just as you'd expect them to be evaluated but without all the bureaucracy.

    Condition UB1 checks if the datetime provided is the (inclusive) start / (exclusive) end of a German "Stromtag".
    Condition UB1 will be replaced with the format constraint 932.

    Condition UB2 checks if the datetime provided is the (inclusive) start / (exclusive) end of a German "Gastag".
    Condition UB2 will be replaced with the format constraint 934.

    Condition UB3 checks if the datetime provided is the (inclusive) start / (exclusive) end of a German "Stromtag" if
    the receiver is from division electricity (RC 492) or a "Gastag" if a receiver is from division gas (RC 493).
    Condition UB3 will be replaced with two XOR connected format constraints, each of them coupled to a requirement
    constraint for the respective division.
    """

    def time_condition(self, tokens: List[Token]) -> Tree:
        """
        try to resolve the package using the injected PackageResolver
        """
        time_condition_key = tokens[0].value
        if time_condition_key == 'UB1':
            return Tree('condition', [Token('CONDITION_KEY', '932')])
        if time_condition_key == 'UB2':
            return Tree('condition', [Token('CONDITION_KEY', '934')])
        if time_condition_key == 'UB3':
            return parse_condition_expression_to_tree('[932][492]X[934][493]')
        raise NotImplementedError(f"The time_condition '{time_condition_key}' is not implemented")