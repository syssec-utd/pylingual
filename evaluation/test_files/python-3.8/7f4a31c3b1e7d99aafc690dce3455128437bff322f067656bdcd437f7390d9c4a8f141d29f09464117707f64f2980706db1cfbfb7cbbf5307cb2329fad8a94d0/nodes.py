from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Optional, Sequence, Tuple, Union
from pydantic.dataclasses import dataclass

class NodeVisitor:
    """Base class for all Choixe visitors. A visitor can be seen as a special recursive
    function that transforms a `Node` (i.e. an element of a syntax tree) into something
    else, depending on the implementation.

    A `NodeVisitor` implements a variation of the Visitor design pattern on a generic
    `Node` object, i.e. an element in the Choixe AST. In particular, visiting methods
    can return values, providing an easier way to use visitors to produce an output.

    This basic node visitor simply forwards the inputs to the outputs, essentially
    performing no operation on the AST.

    All the methods of `NodeVisitor` are called `visit_<node_type>`, they take as input
    the corresponding node object, and they can return anything.
    """

    def _ignore(self, node: Node) -> Any:
        return node

    def visit_dict(self, node: DictNode) -> Any:
        return self._ignore(node)

    def visit_list(self, node: ListNode) -> Any:
        return self._ignore(node)

    def visit_literal(self, node: LiteralNode) -> Any:
        return self._ignore(node)

    def visit_dict_bundle(self, node: DictBundleNode) -> Any:
        return self._ignore(node)

    def visit_str_bundle(self, node: StrBundleNode) -> Any:
        return self._ignore(node)

    def visit_var(self, node: VarNode) -> Any:
        return self._ignore(node)

    def visit_import(self, node: ImportNode) -> Any:
        return self._ignore(node)

    def visit_sweep(self, node: SweepNode) -> Any:
        return self._ignore(node)

    def visit_symbol(self, node: SymbolNode) -> Any:
        return self._ignore(node)

    def visit_instance(self, node: InstanceNode) -> Any:
        return self._ignore(node)

    def visit_model(self, node: ModelNode) -> Any:
        return self._ignore(node)

    def visit_for(self, node: ForNode) -> Any:
        return self._ignore(node)

    def visit_switch(self, node: SwitchNode) -> Any:
        return self._ignore(node)

    def visit_index(self, node: IndexNode) -> Any:
        return self._ignore(node)

    def visit_item(self, node: ItemNode) -> Any:
        return self._ignore(node)

    def visit_uuid(self, node: UuidNode) -> Any:
        return self._ignore(node)

    def visit_date(self, node: DateNode) -> Any:
        return self._ignore(node)

    def visit_cmd(self, node: CmdNode) -> Any:
        return self._ignore(node)

    def visit_tmp_dir(self, node: TmpDirNode) -> Any:
        return self._ignore(node)

    def visit_rand(self, node: RandNode) -> Any:
        return self._ignore(node)

@dataclass
class Node(ABC):
    """A generic element of the Choixe AST, all nodes must implement this interface."""

    @abstractmethod
    def accept(self, visitor: NodeVisitor) -> Any:
        """Accepts an incoming visitor. This method should simply call the respective
        `visit_<node_type>` method of the visiting object, pass `self` as argument
        and forward the result.

        Args:
            visitor (NodeVisitor): The visiting object.

        Returns:
            Any: The visitor result.
        """
        pass

@dataclass
class HashNode(Node):
    """A `HashNode` is a special type of node that is hashable. It represents an
    immutable structure and can generally be used as a dictionary key."""

    def __hash__(self) -> int:
        return hash(tuple(self.__dict__.values()))

    def __eq__(self, __o: object) -> bool:
        return self.__class__ == __o.__class__ and hash(self) == hash(__o)

@dataclass
class DictNode(Node):
    """AST node for Mapping-like structures. Contains a mapping from `HashNode` to `Node`."""
    nodes: Dict[HashNode, Node]

    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_dict(self)

@dataclass(init=False)
class ListNode(Node):
    """AST node for List-like structures. Contains a list of `Node` objects."""
    nodes: Sequence[Node]

    def __init__(self, *nodes: Node) -> None:
        self.nodes = nodes

    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_list(self)

@dataclass(eq=False, unsafe_hash=False)
class LiteralNode(HashNode):
    """An `LiteralNode` contains a single generic hashable python object, like a built-in
    int, float or str."""
    data: Any

    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_literal(self)

    def __hash__(self) -> int:
        if callable(self.data):
            return hash(self.data.__code__)
        return hash(self.data)

@dataclass(init=False, eq=False)
class DictBundleNode(Node):
    """An `DictBundleNode` represents a dictionary union of a nodes collection."""
    nodes: Sequence[Node]

    def __init__(self, *nodes: Node) -> None:
        self.nodes = nodes

    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_dict_bundle(self)

@dataclass(init=False, eq=False)
class StrBundleNode(HashNode):
    """A `StrBundleNode` represents a concatenation of a sequence of strings."""
    nodes: Sequence[HashNode]

    def __init__(self, *nodes: HashNode) -> None:
        self.nodes = nodes

    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_str_bundle(self)

@dataclass(eq=False)
class VarNode(HashNode):
    """A `VarNode` represents a Choixe variable. It has an id and a default value."""
    identifier: HashNode
    default: Optional[HashNode] = None
    env: Optional[HashNode] = None
    help: Optional[LiteralNode] = None

    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_var(self)

@dataclass
class ImportNode(Node):
    """An `ImportNode` represents a Choixe import directive from a filesystem path."""
    path: HashNode

    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_import(self)

@dataclass(init=False, eq=False)
class SweepNode(HashNode):
    """A `SweepNode` represents a Choixe sweep directive from multiple branching options."""
    cases: Sequence[Node]

    def __init__(self, *cases: Node) -> None:
        self.cases = cases

    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_sweep(self)

@dataclass
class SymbolNode(Node):
    """A `SymbolNode` represents a Choixe instance block to import a generic python object."""
    symbol: HashNode

    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_symbol(self)

@dataclass
class InstanceNode(Node):
    """An `InstanceNode` represents a Choixe instance block to get the result of a
    generic python callable object."""
    symbol: HashNode
    args: Union[DictNode, DictBundleNode]

    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_instance(self)

@dataclass
class ModelNode(InstanceNode):

    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_model(self)

@dataclass
class ForNode(Node):
    """A `ForNode` represents a Choixe for loop that iterates over a collection picked
    from the context. A for loop also has an string identifier, that mast be a valid
    python id."""
    iterable: LiteralNode
    body: Node
    identifier: Optional[LiteralNode] = None

    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_for(self)

@dataclass
class SwitchNode(Node):
    value: HashNode
    cases: Sequence[Tuple[Node, Node]]
    default: Optional[Node] = None

    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_switch(self)

@dataclass(eq=False)
class IndexNode(HashNode):
    """An `IndexNode` represents the index of the current iteration of a for loop."""
    identifier: Optional[HashNode] = None

    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_index(self)

@dataclass(eq=False)
class ItemNode(HashNode):
    """An `ItemNode` represents the item of the current iteration of a for loop."""
    identifier: Optional[HashNode] = None

    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_item(self)

@dataclass(eq=False)
class UuidNode(HashNode):
    """An `UuidNode` represents a randomly generated uuid."""

    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_uuid(self)

@dataclass(eq=False)
class DateNode(HashNode):
    """A `DateNode` represents the current datetime with an optional custom format."""
    format: Optional[HashNode] = None

    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_date(self)

@dataclass(eq=False)
class CmdNode(HashNode):
    """A `CmdNode` represents the calling of a system command."""
    command: HashNode

    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_cmd(self)

@dataclass(eq=False)
class TmpDirNode(HashNode):
    """A `TmpDirNode` represents the creation of a temporary directory."""
    name: Optional[HashNode] = None

    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_tmp_dir(self)

@dataclass(init=False)
class RandNode(Node):
    """A `RandNode` represents the creation of a random number."""
    args: Sequence[HashNode] = tuple()
    n: Optional[Node] = None
    pdf: Optional[Node] = None

    def __init__(self, *args: HashNode, **data) -> None:
        super().__init__()
        self.args = args
        self.n = data.get('n')
        self.pdf = data.get('pdf')

    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_rand(self)