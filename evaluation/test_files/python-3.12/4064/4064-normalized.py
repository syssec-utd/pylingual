def layer_permutation(self, layer_partition, layout, qubit_subset):
    """Find a swap circuit that implements a permutation for this layer.

        The goal is to swap qubits such that qubits in the same two-qubit gates
        are adjacent.

        Based on Sergey Bravyi's algorithm.

        The layer_partition is a list of (qu)bit lists and each qubit is a
        tuple (qreg, index).
        The layout is a dict mapping qubits in the circuit to qubits in the
        coupling graph and represents the current positions of the data.
        The qubit_subset is the subset of qubits in the coupling graph that
        we have chosen to map into.
        The coupling is a CouplingGraph.
        TRIALS is the number of attempts the randomized algorithm makes.

        Returns: success_flag, best_circ, best_d, best_layout, trivial_flag

        If success_flag is True, then best_circ contains a DAGCircuit with
        the swap circuit, best_d contains the depth of the swap circuit, and
        best_layout contains the new positions of the data qubits after the
        swap circuit has been applied. The trivial_flag is set if the layer
        has no multi-qubit gates.
        """
    if self.seed is None:
        self.seed = np.random.randint(0, np.iinfo(np.int32).max)
    rng = np.random.RandomState(self.seed)
    rev_layout = {b: a for a, b in layout.items()}
    gates = []
    for layer in layer_partition:
        if len(layer) > 2:
            raise TranspilerError('Layer contains >2 qubit gates')
        elif len(layer) == 2:
            gates.append(tuple(layer))
    dist = sum([self.coupling_map.distance(layout[g[0]][1], layout[g[1]][1]) for g in gates])
    if dist == len(gates):
        circ = DAGCircuit()
        circ.add_qreg(QuantumRegister(self.coupling_map.size(), 'q'))
        return (True, circ, 0, layout, bool(gates))
    n = self.coupling_map.size()
    best_d = sys.maxsize
    best_circ = None
    best_layout = None
    QR = QuantumRegister(self.coupling_map.size(), 'q')
    for _ in range(self.trials):
        trial_layout = layout.copy()
        rev_trial_layout = rev_layout.copy()
        trial_circ = DAGCircuit()
        trial_circ.add_qreg(QR)
        xi = {}
        for i in self.coupling_map.physical_qubits:
            xi[QR, i] = {}
        for i in self.coupling_map.physical_qubits:
            i = (QR, i)
            for j in self.coupling_map.physical_qubits:
                j = (QR, j)
                scale = 1 + rng.normal(0, 1 / n)
                xi[i][j] = scale * self.coupling_map.distance(i[1], j[1]) ** 2
                xi[j][i] = xi[i][j]
        d = 1
        circ = DAGCircuit()
        circ.add_qreg(QR)
        identity_wire_map = {(QR, j): (QR, j) for j in range(n)}
        while d < 2 * n + 1:
            qubit_set = set(qubit_subset)
            while qubit_set:
                min_cost = sum([xi[trial_layout[g[0]]][trial_layout[g[1]]] for g in gates])
                progress_made = False
                for e in self.coupling_map.get_edges():
                    e = [(QR, edge) for edge in e]
                    if e[0] in qubit_set and e[1] in qubit_set:
                        new_layout = trial_layout.copy()
                        new_layout[rev_trial_layout[e[0]]] = e[1]
                        new_layout[rev_trial_layout[e[1]]] = e[0]
                        rev_new_layout = rev_trial_layout.copy()
                        rev_new_layout[e[0]] = rev_trial_layout[e[1]]
                        rev_new_layout[e[1]] = rev_trial_layout[e[0]]
                        new_cost = sum([xi[new_layout[g[0]]][new_layout[g[1]]] for g in gates])
                        if new_cost < min_cost:
                            progress_made = True
                            min_cost = new_cost
                            opt_layout = new_layout
                            rev_opt_layout = rev_new_layout
                            opt_edge = e
                if progress_made:
                    qubit_set.remove(opt_edge[0])
                    qubit_set.remove(opt_edge[1])
                    trial_layout = opt_layout
                    rev_trial_layout = rev_opt_layout
                    circ.apply_operation_back(SwapGate(), [(opt_edge[0][0], opt_edge[0][1]), (opt_edge[1][0], opt_edge[1][1])], [])
                else:
                    break
            dist = sum([self.coupling_map.distance(trial_layout[g[0]][1], trial_layout[g[1]][1]) for g in gates])
            if dist == len(gates):
                trial_circ.compose_back(circ, identity_wire_map)
                break
            d += 1
        dist = sum([self.coupling_map.distance(trial_layout[g[0]][1], trial_layout[g[1]][1]) for g in gates])
        if dist == len(gates):
            if d < best_d:
                best_circ = trial_circ
                best_layout = trial_layout
            best_d = min(best_d, d)
    if best_circ is None:
        return (False, None, None, None, False)
    return (True, best_circ, best_d, best_layout, False)