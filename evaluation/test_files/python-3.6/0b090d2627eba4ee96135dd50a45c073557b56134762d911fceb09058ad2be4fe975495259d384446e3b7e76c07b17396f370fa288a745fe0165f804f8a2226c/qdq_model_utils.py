import onnx
from ..onnx_model_utils import get_producer_consumer_maps, iterate_graph_per_graph_func

def _duplicate_dq_nodes_with_multiple_consumers(graph: onnx.GraphProto, **kwargs):
    updated_graphs = kwargs['updated_graphs']
    node_to_consumers = kwargs['node_to_consumers']
    validate_updates = kwargs['validate_updates']
    nodes_to_update = []
    for node in filter(lambda node: node.op_type == 'DequantizeLinear', graph.node):
        consumers = node_to_consumers[node] if node in node_to_consumers else []
        if len(consumers) > 1:
            if not all((consumer in graph.node for consumer in consumers)):
                raise IndexError('DequantizeLinear node output is consumed by a subgraph. This is not currently supported.')
            nodes_to_update.append(node)
    if validate_updates:
        if nodes_to_update:
            raise ValueError('Graph still has DequantizeLinear nodes with multiple consumers.')
        return
    if nodes_to_update:
        dup_idx = 0
        new_graph = onnx.GraphProto()
        graph_outputs = set([output.name for output in graph.output])
        for node in graph.node:
            new_graph.node.append(node)
            if node in nodes_to_update:
                is_graph_output = node.output[0] in graph_outputs
                start_idx = 0 if is_graph_output else 1
                consumers = list(node_to_consumers[node])[start_idx:]
                for (idx, consumer) in enumerate(consumers):
                    duplicate = onnx.NodeProto()
                    duplicate.CopyFrom(node)
                    duplicate.name += f'/qdq_utils_dup_{dup_idx}'
                    orig_output = node.output[0]
                    new_output = f'{orig_output}/qdq_utils_dup_{idx}'
                    duplicate.output[0] = new_output
                    for (input_idx, input_name) in enumerate(consumer.input):
                        if input_name == orig_output:
                            consumer.input[input_idx] = new_output
                    new_graph.node.append(duplicate)
                    dup_idx += 1
        del graph.node[:]
        graph.node.extend(new_graph.node)
        updated_graphs.append(graph)

def fix_dq_nodes_with_multiple_consumers(model):
    """
    Update a model if any DequantizeLinear nodes have multiple consumers.
    The QDQ node unit processing is overly complicated if this is the case, as the DQ node would be in multiple units,
    and the units may end up in different partitions at runtime.
    :param model: QDQ model to update
    """
    (node_to_producers, node_to_consumers) = get_producer_consumer_maps(model.graph)
    updated_graphs = []
    iterate_graph_per_graph_func(model.graph, _duplicate_dq_nodes_with_multiple_consumers, node_to_consumers=node_to_consumers, validate_updates=False, updated_graphs=updated_graphs)
    if updated_graphs:
        updated_graphs = []
        (node_to_producers, node_to_consumers) = get_producer_consumer_maps(model.graph)
        iterate_graph_per_graph_func(model.graph, _duplicate_dq_nodes_with_multiple_consumers, node_to_consumers=node_to_consumers, validate_updates=True, updated_graphs=updated_graphs)
        onnx.checker.check_model(model)
        _ = onnx.shape_inference.infer_shapes(model)