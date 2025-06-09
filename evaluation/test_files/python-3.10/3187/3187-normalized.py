def head_and_tail_print(self, n=5):
    """Display the first and last n elements of a DataFrame."""
    from IPython import display
    display.display(display.HTML(self._head_and_tail_table(n)))