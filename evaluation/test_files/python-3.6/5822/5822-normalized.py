def load_command_line_configuration(self, args=None):
    """Override configuration according to command line parameters

        return additional arguments
        """
    with _patch_optparse():
        if args is None:
            args = sys.argv[1:]
        else:
            args = list(args)
        (options, args) = self.cmdline_parser.parse_args(args=args)
        for provider in self._nocallback_options:
            config = provider.config
            for attr in config.__dict__.keys():
                value = getattr(options, attr, None)
                if value is None:
                    continue
                setattr(config, attr, value)
        return args