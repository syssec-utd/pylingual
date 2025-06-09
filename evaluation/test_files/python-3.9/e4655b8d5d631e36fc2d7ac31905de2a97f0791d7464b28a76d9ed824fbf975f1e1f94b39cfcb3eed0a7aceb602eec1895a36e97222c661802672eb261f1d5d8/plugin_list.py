class PluginList:

    def __init__(self, plugins):
        self._plugins = plugins

    def on_train_start(self, trainer, model):
        for plugin in self._plugins:
            if hasattr(plugin, 'on_train_start'):
                plugin.on_train_start(trainer, model)

    def on_train_end(self, trainer, model):
        for plugin in self._plugins:
            if hasattr(plugin, 'on_train_end'):
                plugin.on_train_end(trainer, model)

    def on_train_epoch_start(self, trainer, model, epoch_index):
        for plugin in self._plugins:
            if hasattr(plugin, 'on_train_epoch_start'):
                plugin.on_train_epoch_start(trainer, model, epoch_index)

    def on_train_epoch_end(self, trainer, model, epoch_index):
        for plugin in self._plugins:
            if hasattr(plugin, 'on_train_epoch_end'):
                plugin.on_train_epoch_end(trainer, model, epoch_index)

    def on_train_batch_start(self, trainer, model, batch, batch_index):
        for plugin in self._plugins:
            if hasattr(plugin, 'on_train_batch_start'):
                batch = plugin.on_train_batch_start(trainer, model, batch, batch_index)
        return batch

    def on_train_batch_end(self, trainer, model, loss, batch, batch_index):
        for plugin in self._plugins:
            if hasattr(plugin, 'on_train_batch_end'):
                plugin.on_train_batch_end(trainer, model, loss, batch, batch_index)

    def on_train_backward_start(self, trainer, model, loss):
        for plugin in self._plugins:
            if hasattr(plugin, 'on_train_backward_start'):
                loss = plugin.on_train_backward_start(trainer, model, loss)
        return loss

    def on_validation_start(self, trainer, model):
        for plugin in self._plugins:
            if hasattr(plugin, 'on_validation_start'):
                plugin.on_validation_start(trainer, model)

    def on_validation_end(self, trainer, model):
        for plugin in self._plugins:
            if hasattr(plugin, 'on_validation_end'):
                plugin.on_validation_end(trainer, model)

    def on_validation_batch_start(self, trainer, model, batch, batch_index):
        for plugin in self._plugins:
            if hasattr(plugin, 'on_validation_batch_start'):
                batch = plugin.on_validation_batch_start(trainer, model, batch, batch_index)
        return batch

    def on_validation_batch_end(self, trainer, model, loss, batch, batch_index):
        for plugin in self._plugins:
            if hasattr(plugin, 'on_validation_batch_end'):
                plugin.on_validation_batch_end(trainer, model, loss, batch, batch_index)