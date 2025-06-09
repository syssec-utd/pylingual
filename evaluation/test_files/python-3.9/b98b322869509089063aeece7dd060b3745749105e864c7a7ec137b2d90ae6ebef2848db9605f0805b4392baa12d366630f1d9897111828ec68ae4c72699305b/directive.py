from abc import ABC
from xformula.syntax.grammar.definitions.abc import Definition, DefinitionType
__all__ = ['Directive']

class Directive(Definition, ABC):

    class Meta(Definition.Meta):
        abstract = True
        type = DefinitionType.DIRECTIVE