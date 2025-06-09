def save_figure(self):
    """
        This function programs the button to save the figure displayed
        and save it in a png file in the current repository.
        """
    '\n        Increment the name of the figure in order to not erase the previous figure if the user use always this method.\n        The png file is put in the "Artists_saved" file localized in the "planarradpy" folder.\n        '
    default_name = 'Default_figure.png'
    self.ui.graphic_widget.canvas.print_figure(default_name)
    src = './' + default_name
    dst = './Artists_saved'
    os.system('mv' + ' ' + src + ' ' + dst)