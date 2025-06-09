def register_training_hooks(self, lr_config, optimizer_config=None, checkpoint_config=None, log_config=None):
    """Register default hooks for training.

        Default hooks include:

        - LrUpdaterHook
        - OptimizerStepperHook
        - CheckpointSaverHook
        - IterTimerHook
        - LoggerHook(s)
        """
    if optimizer_config is None:
        optimizer_config = {}
    if checkpoint_config is None:
        checkpoint_config = {}
    self.register_lr_hooks(lr_config)
    self.register_hook(self.build_hook(optimizer_config, OptimizerHook))
    self.register_hook(self.build_hook(checkpoint_config, CheckpointHook))
    self.register_hook(IterTimerHook())
    if log_config is not None:
        self.register_logger_hooks(log_config)