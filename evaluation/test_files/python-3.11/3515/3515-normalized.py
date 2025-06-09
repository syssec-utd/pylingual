def run(self, data_loaders, workflow, max_epochs, **kwargs):
    """Start running.

        Args:
            data_loaders (list[:obj:`DataLoader`]): Dataloaders for training
                and validation.
            workflow (list[tuple]): A list of (phase, epochs) to specify the
                running order and epochs. E.g, [('train', 2), ('val', 1)] means
                running 2 epochs for training and 1 epoch for validation,
                iteratively.
            max_epochs (int): Total training epochs.
        """
    assert isinstance(data_loaders, list)
    assert mmcv.is_list_of(workflow, tuple)
    assert len(data_loaders) == len(workflow)
    self._max_epochs = max_epochs
    work_dir = self.work_dir if self.work_dir is not None else 'NONE'
    self.logger.info('Start running, host: %s, work_dir: %s', get_host_info(), work_dir)
    self.logger.info('workflow: %s, max: %d epochs', workflow, max_epochs)
    self.call_hook('before_run')
    while self.epoch < max_epochs:
        for i, flow in enumerate(workflow):
            mode, epochs = flow
            if isinstance(mode, str):
                if not hasattr(self, mode):
                    raise ValueError('runner has no method named "{}" to run an epoch'.format(mode))
                epoch_runner = getattr(self, mode)
            elif callable(mode):
                epoch_runner = mode
            else:
                raise TypeError('mode in workflow must be a str or callable function, not {}'.format(type(mode)))
            for _ in range(epochs):
                if mode == 'train' and self.epoch >= max_epochs:
                    return
                epoch_runner(data_loaders[i], **kwargs)
    time.sleep(1)
    self.call_hook('after_run')