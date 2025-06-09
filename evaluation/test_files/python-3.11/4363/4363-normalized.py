def run(self, dag):
    """Return a circuit with a barrier before last measurements."""
    final_op_types = ['measure', 'barrier']
    final_ops = []
    for candidate_node in dag.named_nodes(*final_op_types):
        is_final_op = True
        for _, child_successors in dag.bfs_successors(candidate_node):
            if any((suc.type == 'op' and suc.name not in final_op_types for suc in child_successors)):
                is_final_op = False
                break
        if is_final_op:
            final_ops.append(candidate_node)
    if not final_ops:
        return dag
    barrier_layer = DAGCircuit()
    for qreg in dag.qregs.values():
        barrier_layer.add_qreg(qreg)
    for creg in dag.cregs.values():
        barrier_layer.add_creg(creg)
    final_qubits = set((final_op.qargs[0] for final_op in final_ops))
    barrier_layer.apply_operation_back(Barrier(len(final_qubits)), list(final_qubits), [])
    ordered_final_nodes = [node for node in dag.topological_op_nodes() if node in set(final_ops)]
    for final_node in ordered_final_nodes:
        barrier_layer.apply_operation_back(final_node.op, final_node.qargs, final_node.cargs)
    for final_op in final_ops:
        dag.remove_op_node(final_op)
    dag.extend_back(barrier_layer)
    adjacent_pass = MergeAdjacentBarriers()
    return adjacent_pass.run(dag)