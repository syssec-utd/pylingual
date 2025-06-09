def build_graph(self, regularizers=()):
    """Connect the layers in this network to form a computation graph.

        Parameters
        ----------
        regularizers : list of :class:`theanets.regularizers.Regularizer`
            A list of the regularizers to apply while building the computation
            graph.

        Returns
        -------
        outputs : list of Theano variables
            A list of expressions giving the output of each layer in the graph.
        updates : list of update tuples
            A list of updates that should be performed by a Theano function that
            computes something using this graph.
        """
    key = self._hash(regularizers)
    if key not in self._graphs:
        util.log('building computation graph')
        for loss in self.losses:
            loss.log()
        for reg in regularizers:
            reg.log()
        outputs = {}
        updates = []
        for layer in self.layers:
            out, upd = layer.connect(outputs)
            for reg in regularizers:
                reg.modify_graph(out)
            outputs.update(out)
            updates.extend(upd)
        self._graphs[key] = (outputs, updates)
    return self._graphs[key]