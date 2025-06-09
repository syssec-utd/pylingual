def registerEventHandlers(self):
    """
        Registers needed keybinds and schedules the :py:meth:`update` Method.
        
        You can control what keybinds are used via the :confval:`controls.controls.forward` etc. Configuration Values.
        """
    self.peng.keybinds.add(self.peng.cfg['controls.controls.forward'], 'peng3d:actor.%s.player.controls.forward' % self.actor.uuid, self.on_fwd_down, False)
    self.peng.keybinds.add(self.peng.cfg['controls.controls.backward'], 'peng3d:actor.%s.player.controls.backward' % self.actor.uuid, self.on_bwd_down, False)
    self.peng.keybinds.add(self.peng.cfg['controls.controls.strafeleft'], 'peng3d:actor.%s.player.controls.strafeleft' % self.actor.uuid, self.on_left_down, False)
    self.peng.keybinds.add(self.peng.cfg['controls.controls.straferight'], 'peng3d:actor.%s.player.controls.straferight' % self.actor.uuid, self.on_right_down, False)
    pyglet.clock.schedule_interval(self.update, 1.0 / 60)