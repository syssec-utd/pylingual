import attrs
from .base import Element, __compiler__, render
__t__ = __compiler__.compile('{\n{{#each map}}\n    {{{@key}}} = {{{render this}}}\n{{/each}}\n}')

@attrs.define
class AstMap(Element):
    map: dict[str, Element] = attrs.field(factory=dict)

    def set(self, key: str, el: Element) -> None:
        self.map[key] = el

    def get(self, key: str) -> Element | None:
        return self.map.get(key)

    def render(self) -> str:
        return __t__(self, helpers={'render': render})