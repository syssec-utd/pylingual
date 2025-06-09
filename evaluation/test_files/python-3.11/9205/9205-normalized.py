def learning_function(self):
    """
        Get the learning function.
        :param func:
        :return:
        """
    network_updates = list(self.network.updates) + list(self.network.training_updates)
    learning_updates = list(self._learning_updates())
    update_list = network_updates + learning_updates
    logging.info('network updates: %s' % ' '.join(map(str, [x[0] for x in network_updates])))
    logging.info('learning updates: %s' % ' '.join(map(str, [x[0] for x in learning_updates])))
    variables = self.network.input_variables + self.network.target_variables
    givens = None
    return theano.function(variables, map(lambda v: theano.Out(v, borrow=True), self.training_variables), updates=update_list, allow_input_downcast=True, mode=self.config.get('theano_mode', None), givens=givens)