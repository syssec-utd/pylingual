def cat_handler(self, args):
    """Handler for cat command"""
    self.validate('cmd|s3', args)
    source = args[1]
    self.s3handler().print_files(source)