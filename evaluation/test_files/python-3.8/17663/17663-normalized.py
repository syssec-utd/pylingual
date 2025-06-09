def main_source(self, operator, value=None):
    """
        Execute Main.Source.

        Returns int
        """
    try:
        source = int(self.exec_command('main', 'source', operator, value))
        return source
    except (ValueError, TypeError):
        pass
    return None