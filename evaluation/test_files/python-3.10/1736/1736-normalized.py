def merge_checkpoint(input_graph, checkpoint, output_node_names, output_graph, sess):
    """
    Get the variable values from the checkpoint file, and merge them to the GraphDef file
    Args:
        input_graph: the GraphDef file, doesn't contain variable values
        checkpoint: the checkpoint file
        output_node_names: A list of string, the output names
        output_graph: String of the location and the name of the
            output graph
    """
    restore_op_name = 'save/restore_all'
    filename_tensor_name = 'save/Const:0'
    input_graph_def = graph_pb2.GraphDef()
    with gfile.FastGFile(input_graph, 'r') as f:
        text_format.Merge(f.read().decode('utf-8'), input_graph_def)
    for node in input_graph_def.node:
        node.device = ''
    importer.import_graph_def(input_graph_def, name='')
    sess.run([restore_op_name], {filename_tensor_name: checkpoint})
    output_graph_def = graph_util.convert_variables_to_constants(sess, input_graph_def, output_node_names, variable_names_blacklist='')
    with gfile.GFile(output_graph, 'wb') as f:
        f.write(output_graph_def.SerializeToString())