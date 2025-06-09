def set_secondary_inputs(self, channel_dict):
    """ Adds secondary inputs to the start of the pipeline.

        This channels are inserted into the pipeline file as they are
        provided in the values of the argument.

        Parameters
        ----------
        channel_dict : dict
            Each entry should be <parameter>: <channel string>.
        """
    logger.debug('Setting secondary inputs: {}'.format(channel_dict))
    secondary_input_str = '\n'.join(list(channel_dict.values()))
    self._context = {**self._context, **{'secondary_inputs': secondary_input_str}}