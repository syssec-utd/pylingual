def mainloop(self, local_ns=None, module=None, stack_depth=0, display_banner=None, global_ns=None):
    """Embeds IPython into a running python program.

        Input:

          - header: An optional header message can be specified.

          - local_ns, module: working local namespace (a dict) and module (a
          module or similar object). If given as None, they are automatically
          taken from the scope where the shell was called, so that
          program variables become visible.

          - stack_depth: specifies how many levels in the stack to go to
          looking for namespaces (when local_ns or module is None).  This
          allows an intermediate caller to make sure that this function gets
          the namespace from the intended level in the stack.  By default (0)
          it will get its locals and globals from the immediate caller.

        Warning: it's possible to use this in a program which is being run by
        IPython itself (via %run), but some funny things will happen (a few
        globals get overwritten). In the future this will be cleaned up, as
        there is no fundamental reason why it can't work perfectly."""
    if global_ns is not None and module is None:

        class DummyMod(object):
            """A dummy module object for embedded IPython."""
            pass
        warnings.warn('global_ns is deprecated, use module instead.', DeprecationWarning)
        module = DummyMod()
        module.__dict__ = global_ns
    if (local_ns is None or module is None) and self.default_user_namespaces:
        call_frame = sys._getframe(stack_depth).f_back
        if local_ns is None:
            local_ns = call_frame.f_locals
        if module is None:
            global_ns = call_frame.f_globals
            module = sys.modules[global_ns['__name__']]
    orig_user_module = self.user_module
    orig_user_ns = self.user_ns
    if module is not None:
        self.user_module = module
    if local_ns is not None:
        self.user_ns = local_ns
        self.init_user_ns()
    self.set_completer_frame()
    with nested(self.builtin_trap, self.display_trap):
        self.interact(display_banner=display_banner)
    if local_ns is not None:
        for name in self.user_ns_hidden:
            local_ns.pop(name, None)
    self.user_module = orig_user_module
    self.user_ns = orig_user_ns