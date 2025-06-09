import copy
from typing import List
from model_compression_toolkit.core.common import Graph, BaseNode
from model_compression_toolkit.core.common.constants import DEFAULT_CANDIDATE_BITWIDTH
from model_compression_toolkit.core.common.quantization.candidate_node_quantization_config import CandidateNodeQuantizationConfig

def filter_nodes_candidates(graph_to_filter: Graph):
    """
    Filters the graph's nodes candidates configuration list.
    We apply this after mark activation operation to eliminate nodes that their activation are no longer being quantized
    from the mixed-precision search.
    Updating the lists is preformed inplace on the graph object.

    Args:
        graph_to_filter: Graph for which to add quantization info to each node.
    """
    graph = copy.deepcopy(graph_to_filter)
    nodes = list(graph.nodes)
    for n in nodes:
        n.candidates_quantization_cfg = filter_node_candidates(node=n)
    return graph

def filter_node_candidates(node: BaseNode) -> List[CandidateNodeQuantizationConfig]:
    """
    Updates a node's candidates configuration list.
    If the node's weights quantization is disabled (or it only has activations to quantize), then the updated list
    will have a candidate with any of the different original activation bitwidths candidates and a default value
    for its weights bitwidth (that doesn't have any impact on the quantization or the mixed-precision search.
    If the node's activation quantization is disabled, the same filtering applied for the weights bitwidth candidates.

    Args:
        node: Node to set its quantization configurations.
    """
    filtered_candidates = copy.deepcopy(node.candidates_quantization_cfg)
    if not node.is_activation_quantization_enabled():
        seen_candidates = set()
        filtered_candidates = [candidate for candidate in filtered_candidates if candidate.weights_quantization_cfg not in seen_candidates and (not seen_candidates.add(candidate.weights_quantization_cfg))]
        for c in filtered_candidates:
            c.activation_quantization_cfg.activation_n_bits = DEFAULT_CANDIDATE_BITWIDTH
    elif not node.is_weights_quantization_enabled():
        seen_candidates = set()
        filtered_candidates = [candidate for candidate in filtered_candidates if candidate.activation_quantization_cfg not in seen_candidates and (not seen_candidates.add(candidate.activation_quantization_cfg))]
        for c in filtered_candidates:
            c.weights_quantization_cfg.weights_n_bits = DEFAULT_CANDIDATE_BITWIDTH
    return filtered_candidates