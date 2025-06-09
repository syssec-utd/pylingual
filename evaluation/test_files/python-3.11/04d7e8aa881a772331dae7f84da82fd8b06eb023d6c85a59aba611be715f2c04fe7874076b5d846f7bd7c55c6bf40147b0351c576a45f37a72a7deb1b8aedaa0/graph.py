from __future__ import annotations
from abc import abstractmethod, ABC
from dataclasses import dataclass
from typing import Set, Dict, Any, List, Optional
import networkx as nx
from graphviz import Digraph
from entropylab.pipeline.api.execution import EntropyContext

@dataclass(frozen=True, eq=True)
class Output:
    """
    Node output respresentation that contain the node and the output name
    """
    node: Node
    name: str

@dataclass
class RetryBehavior:
    """
    Attributes:
        number_of_attempts: the maximum number of retries.
        wait_time: the initial wait time between each attempt [seconds].
        backoff: a factor that multiplies the delay on each attempt (1 is no backoff).
        added_delay: delay that is added on each attempt [seconds].
        max_wait_time: optional maximum delay.
    """
    number_of_attempts: float = 5
    wait_time: float = 10
    backoff: float = 2
    added_delay: float = 0
    max_wait_time: Optional[float] = None

class Node(ABC):
    """
    An abstract class for Entropy graph node.
    Node is defined by some functionality, input and outputs.
    Different implementations of node can be created, and connected one to the other.
    """

    def __init__(self, label: str=None, input_vars: Dict[str, Output]=None, output_vars: Set[str]=None, must_run_after: Set[Node]=None, save_results: bool=True, retry_on_error: RetryBehavior=None):
        """
            An abstract class for Entropy graph node.
        :param label: node label
        :param input_vars: dictionary of node inputs, keys are input names.
                        the input values should be defined as the following:
                            >>>input_vars={"a": node.outputs["x"]}
        :param output_vars: a set of outputs name. The given python function should
                        return a dictionary, which it's keys are the same as output vars
        :param must_run_after: A set of nodes. If those nodes are in the same graph,
                            current node will run after they finish execution.
        :param save_results: True to save the node outputs to results db.
        """
        self._label = label
        self._input_vars = input_vars
        if self._input_vars is None:
            self._input_vars = {}
        self._output_vars: Set[str] = output_vars
        if self._output_vars is None:
            self._output_vars = {}
        self._must_run_after: Set[Node] = must_run_after
        if self._must_run_after is None:
            self._must_run_after = {}
        self._save_results = save_results
        self._retry_on_error = retry_on_error

    @property
    def label(self) -> str:
        """
        :return: node label
        """
        return self._label

    @property
    def outputs(self) -> Dict[str, Output]:
        """
        :return: a dictionary of outputs representations, indexed by name
        """
        return {output_name: Output(self, output_name) for output_name in self._output_vars}

    def add_input(self, name: str, parent_node_output: Output):
        """
            adds a new input to current node
        :param name: input name
        :param parent_node_output: the parent node output representation
        """
        if name in self._input_vars:
            raise KeyError(f'Input {name} already exist')
        self._input_vars[name] = parent_node_output

    def get_parents(self) -> List[Node]:
        """
        :return: list of all parent nodes
        """
        return list(set([var.node for var in self._input_vars.values()])) + list(self._must_run_after)

    def get_inputs(self) -> List[Output]:
        """
        :return: list of all input, as the parent node output representations
        """
        return list(self._input_vars.values())

    def get_inputs_by_name(self) -> Dict[str, Output]:
        """
        :return: a dictionary of node inputs as the parent node output representation,
                indexed by name
        """
        return self._input_vars

    @abstractmethod
    def _execute(self, input_values: Dict[str, Any], context: EntropyContext, is_last, **kwargs) -> Dict[str, Any]:
        """
            Execute the node - run the node function with the given input and context.
            The abstract method _execute should be implemented by all subclasses.
        :param input_values: a dictionary of inputs, indexed by input name
        :param context: Entropy context of the specific node.
        :param is_last: True if this is the last node of the graph.
        :param kwargs: extra key word arguments passed by the user in definition.run function
        """
        pass

    @abstractmethod
    async def _execute_async(self, input_values: Dict[str, Any], context: EntropyContext, is_last, **kwargs) -> Dict[str, Any]:
        """
            Execute the node - run the node function with the given input and context.
            The abstract method _execute_async should be implemented by all subclasses.
            the method is an async method, so it can run in asyncio context.
        :param input_values: a dictionary of inputs, indexed by input name
        :param context: Entropy context of the specific node.
        :param is_last: True if this is the last node of the graph.
        :param kwargs: extra key word arguments passed by the user in definition.run function
        """
        pass

    def ancestors(self) -> Set[Node]:
        """
        :return: a set of node's ancestors, including current node
        """
        parents: Set[Node] = set([var.node for var in self._input_vars.values()] + list(self._must_run_after))
        ancestors = parents.copy()
        ancestors.add(self)
        for anc in parents:
            ancestors.update(anc.ancestors())
        return ancestors

    def _should_save_results(self):
        return self._save_results

    def _retry_on_error_function(self) -> RetryBehavior:
        return self._retry_on_error

@dataclass(frozen=True, eq=True)
class _NodeExecutionInfo:
    node: Node
    is_key_node: bool

class GraphHelper:
    """
    Class representing a graph, with relevant graph functions and algorithms
    """

    def __init__(self, nodes: Set[_NodeExecutionInfo]) -> None:
        """
            Class representing a graph, with relevant graph functions and algorithms
        :param nodes: complete set of nodes that assembles the graph
        """
        super().__init__()
        self._nodes: Set[_NodeExecutionInfo] = nodes

    @property
    def nodes(self) -> Set[Node]:
        """
            a set of all graph nodes
        :return:
        """
        return set([node.node for node in self._nodes])

    @property
    def leaves(self) -> Set[Node]:
        """
            a set of graph leaves
        :return:
        """
        end_nodes = {node.node for node in self._nodes}
        for node in self._nodes:
            for parent in node.node.get_parents():
                if parent in end_nodes:
                    end_nodes.remove(parent)
        return end_nodes

    def export_dot_graph(self) -> Digraph:
        """
        Converts the graph into DOT graph format
        :return: str
        """
        visited_labels = {}
        node_labels = {}

        def unique_label(node):
            if node in node_labels:
                return node_labels[node]
            if node.label in visited_labels:
                index = visited_labels[node.label] + 1
                visited_labels[node.label] = index
                node_labels[node] = f'{node.label}_{str(index)}'
            else:
                visited_labels[node.label] = 1
                node_labels[node] = node.label
            return node_labels[node]
        dot = Digraph()
        nodes = self._nodes
        for node in nodes:
            dot.node(unique_label(node.node), shape='box')
        for node in nodes:
            parents = node.node.get_parents()
            inputs = node.node.get_inputs()
            for parent in parents:
                input_names = [input.name for input in filter(lambda input: input.node == parent, inputs)]
                dot.edge(unique_label(parent), unique_label(node.node), ','.join(input_names))
        dot.graph_attr['rankdir'] = 'LR'
        return dot

    def nodes_in_topological_order(self) -> List[Node]:
        """
        returns a complete list of graph nodes, sorted in a topological order
        """
        g = nx.DiGraph()
        nodes = self.nodes
        for node in nodes:
            g.add_node(node)
        for node in nodes:
            for parent in node.get_parents():
                g.add_edge(parent, node)
        sorted_list = nx.topological_sort(g)
        return list(sorted_list)