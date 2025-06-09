"""Graph simulator

Graph state simulator, according to
M. Elliot, B. Eastin & C. Caves,
    JPhysA 43, 025301 (2010) and PRA 77, 042307 (2008)

"""
import networkx as nx
import numpy as np
from graphix.clifford import CLIFFORD_MUL, CLIFFORD_HSZ_DECOMPOSITION
from graphix.sim.statevec import Statevec
from graphix.ops import Ops

class GraphState(nx.Graph):
    """Graph state simulator

    Performs Pauli measurements on graph states.
    Inherits methods and attributes from networkx.Graph.

    ref: M. Elliot, B. Eastin & C. Caves, JPhysA 43, 025301 (2010)
    and PRA 77, 042307 (2008)

    Each node has attributes:
        :`hollow`: True if node is hollow
        :`sign`: True if node has negative sign
        :`loop`: True if node has loop
    """

    def __init__(self, nodes=None, edges=None, vops=None):
        """
        Parameters
        ----------
        nodes : iterable container
            A container of nodes (list, dict, etc)
        edges : list
            list of tuples (i,j) for pairs to be entangled.
        vops : dict
            dict of local Clifford gates with keys for node indices and
            values for Clifford index (see graphix.clifford.CLIFFORD)
        """
        super().__init__()
        if nodes is not None:
            self.add_nodes_from(nodes)
        if edges is not None:
            self.add_edges_from(edges)
        if vops is not None:
            self.apply_vops(vops)

    def apply_vops(self, vops):
        """Apply local Clifford operators to the graph state from a dictionary

        Parameters
        ----------
            vops : dict
                dict containing node indices as keys and
                local Clifford indices as values (see graphix.clifford.CLIFFORD)
        """
        for (node, vop) in vops.items():
            for lc in reversed(CLIFFORD_HSZ_DECOMPOSITION[vop]):
                if lc == 3:
                    self.z(node)
                elif lc == 6:
                    self.h(node)
                elif lc == 4:
                    self.s(node)

    def add_nodes_from(self, nodes):
        """Add nodes and initialize node properties.

        Parameters
        ----------
        nodes : iterable container
            A container of nodes (list, dict, etc)
        """
        super().add_nodes_from(nodes, loop=False, sign=False, hollow=False)

    def add_edges_from(self, edges):
        """Add edges and initialize node properties of newly added nodes.

        Parameters
        ----------
        edges : iterable container
            must be given as list of 2-tuples (u, v)
        """
        super().add_edges_from(edges)
        for i in self.nodes:
            if 'loop' not in self.nodes[i]:
                self.nodes[i]['loop'] = False
                self.nodes[i]['sign'] = False
                self.nodes[i]['hollow'] = False

    def get_vops(self):
        """Returns a dict containing clifford labels for each nodes.
        labels 0 - 23 specify one of 24 single-qubit Clifford gates.
        see graphq.clifford for the definition of all unitaries.

        Returns
        ----------
        vops : dict
            clifford gate indices as defined in `graphq.clifford`.


        .. seealso:: :mod:`graphix.clifford`
        """
        vops = {}
        for i in self.nodes:
            vop = 0
            if self.nodes[i]['sign']:
                vop = CLIFFORD_MUL[3, vop]
            if self.nodes[i]['loop']:
                vop = CLIFFORD_MUL[4, vop]
            if self.nodes[i]['hollow']:
                vop = CLIFFORD_MUL[6, vop]
            vops[i] = vop
        return vops

    def flip_fill(self, node):
        """Flips the fill (local H) of a node.

        Parameters
        ----------
        node : int
            graph node to flip the fill
        """
        self.nodes[node]['hollow'] = not self.nodes[node]['hollow']

    def flip_sign(self, node):
        """Flips the sign (local Z) of a node.
        Note that application of Z gate is different from `flip_sign`
        if there exist an edge from the node.

        Parameters
        ----------
        node : int
            graph node to flip the sign
        """
        self.nodes[node]['sign'] = not self.nodes[node]['sign']

    def advance(self, node):
        """Flips the loop (local S) of a node.
        If the loop already exist, sign is also flipped,
        reflecting the relation SS=Z.
        Note that application of S gate is different from `advance`
        if there exist an edge from the node.

        Parameters
        ----------
        node : int
            graph node to advance the loop.
        """
        if self.nodes[node]['loop']:
            self.nodes[node]['loop'] = False
            self.flip_sign(node)
        else:
            self.nodes[node]['loop'] = True

    def h(self, node):
        """Apply H gate to a qubit (node).

        Parameters
        ----------
        node : int
            graph node to apply H gate
        """
        self.flip_fill(node)

    def s(self, node):
        """Apply S gate to a qubit (node).

        Parameters
        ----------
        node : int
            graph node to apply S gate
        """
        if self.nodes[node]['hollow']:
            if self.nodes[node]['loop']:
                self.flip_fill(node)
                self.nodes['loop'] = False
                self.local_complement(node)
                for i in self.neighbors(node):
                    self.advance(i)
            else:
                self.local_complement(node)
                for i in self.neighbors(node):
                    self.advance(i)
                if self.nodes[node]['sign']:
                    for i in self.neighbors(node):
                        self.flip_sign(i)
        else:
            self.advance(node)

    def z(self, node):
        """Apply Z gate to a qubit (node).

        Parameters
        ----------
        node : int
            graph node to apply Z gate
        """
        if self.nodes[node]['hollow']:
            for i in self.neighbors(node):
                self.flip_sign(i)
            if self.nodes[node]['loop']:
                self.flip_sign(node)
        else:
            self.flip_sign(node)

    def equivalent_graph_E1(self, node):
        """Tranform a graph state to a different graph state
        representing the same stabilizer state.
        This rule applies only to a node with loop.

        Parameters
        ----------
        node1 : int
            A graph node with a loop to apply rule E1
        """
        assert self.nodes[node]['loop']
        self.flip_fill(node)
        self.local_complement(node)
        for i in self.neighbors(node):
            self.advance(i)
        self.flip_sign(node)
        if self.nodes[node]['sign']:
            for i in self.neighbors(node):
                self.flip_sign(i)

    def equivalent_graph_E2(self, node1, node2):
        """Tranform a graph state to a different graph state
        representing the same stabilizer state.
        This rule applies only to two connected nodes without loop.

        Parameters
        ----------
        node1, node2 : int
            connected graph nodes to apply rule E2
        """
        assert (node1, node2) in list(self.edges) or (node2, node1) in list(self.edges)
        assert not self.nodes[node1]['loop'] and (not self.nodes[node2]['loop'])
        self.flip_fill(node1)
        self.flip_fill(node2)
        self.local_complement(node1)
        self.local_complement(node2)
        self.local_complement(node1)
        for i in iter(set(self.neighbors(node1)) & set(self.neighbors(node2))):
            self.flip_sign(i)
        if self.nodes[node1]['sign'] != self.nodes[node2]['sign']:
            if self.nodes[node1]['sign']:
                self.flip_sign(node1)
                for i in self.neighbors(node1):
                    self.flip_sign(i)
            elif self.nodes[node2]['sign']:
                self.flip_sign(node2)
                for i in self.neighbors(node2):
                    self.flip_sign(i)

    def local_complement(self, node):
        """Perform local complementation of a graph

        Parameters
        ----------
        node : int
            chosen node for the local complementation
        """
        g = self.subgraph(list(self.neighbors(node)))
        g_new = nx.complement(g)
        self.remove_edges_from(g.edges)
        self.add_edges_from(g_new.edges)

    def equivalent_fill_node(self, node):
        """Fill the chosen node by graph transformation rules E1 and E2,
        If the selected node is hollow and isolated, it cannot be filled
        and warning is thrown.

        Parameters
        ----------
        node : int
            node to fill.

        Returns
        ----------
        result : int
            if the selected node is hollow and isolated, `result` is 1.
            if filled and isolated, 2.
            otherwise it is 0.
        """
        if self.nodes[node]['hollow']:
            if self.nodes[node]['loop']:
                self.equivalent_graph_E1(node)
                return 0
            else:
                if len(list(self.neighbors(node))) == 0:
                    return 1
                for i in self.neighbors(node):
                    if not self.nodes[i]['loop']:
                        self.equivalent_graph_E2(node, i)
                        return 0
                i = next(self.neighbors(node))
                self.equivalent_graph_E1(i)
                self.equivalent_graph_E1(node)
                return 0
        elif len(list(self.neighbors(node))) == 0:
            return 2
        else:
            return 0

    def measure_x(self, node, choice=0):
        """perform measurement in X basis
        According to original paper, we realise X measurement by
        applying H gate to the measured node before Z measurement.

        Parameters
        ----------
        node : int
            qubit index to be measured
        choice : int, 0 or 1
            choice of measurement outcome. observe (-1)^choice
        """
        self.h(node)
        return self.measure_z(node, choice=choice)

    def measure_y(self, node, choice=0):
        """perform measurement in Y basis
        According to original paper, we realise Y measurement by
        applying S,Z and H gate to the measured node before Z measurement.

        Parameters
        ----------
        node : int
            qubit index to be measured
        choice : int, 0 or 1
            choice of measurement outcome. observe (-1)^choice
        """
        self.s(node)
        self.z(node)
        self.h(node)
        return self.measure_z(node, choice=choice)

    def measure_z(self, node, choice=0):
        """perform measurement in Z basis
        To realize the simple Z measurement on undecorated graph state,
        we first fill the measured node (remove local H gate)

        Parameters
        ----------
        node : int
            qubit index to be measured
        choice : int, 0 or 1
            choice of measurement outcome. observe (-1)^choice
        """
        isolated = self.equivalent_fill_node(node)
        if choice:
            for i in self.neighbors(node):
                self.flip_sign(i)
        if not isolated:
            result = choice
        else:
            result = int(self.nodes[node]['sign'])
        self.remove_node(node)
        return result

    def draw(self, fill_color='C0', **kwargs):
        """Draw decorated graph state.
        Negative nodes are indicated by negative sign of node labels.

        Parameters
        ----------
        fill_color : str, optional
            fill color of nodes
        kwargs : keyword arguments, optional
            additional arguments to supply networkx.draw().
        """
        nqubit = len(self.nodes)
        nodes = list(self.nodes)
        edges = list(self.edges)
        labels = {i: i for i in iter(self.nodes)}
        colors = [fill_color for i in range(nqubit)]
        for i in range(nqubit):
            if self.nodes[nodes[i]]['loop']:
                edges.append((nodes[i], nodes[i]))
            if self.nodes[nodes[i]]['hollow']:
                colors[i] = 'white'
            if self.nodes[nodes[i]]['sign']:
                labels[nodes[i]] = -1 * labels[nodes[i]]
        g = nx.Graph()
        g.add_nodes_from(nodes)
        g.add_edges_from(edges)
        nx.draw(g, labels=labels, node_color=colors, edgecolors='k', **kwargs)

    def to_statevector(self):
        node_list = list(self.nodes)
        nqubit = len(self.nodes)
        gstate = Statevec(nqubit=nqubit)
        imapping = {node_list[i]: i for i in range(nqubit)}
        mapping = [node_list[i] for i in range(nqubit)]
        for (i, j) in self.edges:
            gstate.entangle((imapping[i], imapping[j]))
        for i in range(nqubit):
            if self.nodes[mapping[i]]['sign']:
                gstate.evolve_single(Ops.z, i)
        for i in range(nqubit):
            if self.nodes[mapping[i]]['loop']:
                gstate.evolve_single(Ops.s, i)
        for i in range(nqubit):
            if self.nodes[mapping[i]]['hollow']:
                gstate.evolve_single(Ops.h, i)
        return gstate