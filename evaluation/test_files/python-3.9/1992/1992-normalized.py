def terminate(self):
    """
        Terminate a running cluster.  (Due to a signal.)

        :return none
        """
    for node in self.client_nodes:
        node.terminate()
    for node in self.nodes:
        node.terminate()