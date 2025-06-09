def save(self, name=None, output='png', dirc=None):
    """Saves Bloch sphere to file of type ``format`` in directory ``dirc``.
        Args:
            name (str):
                Name of saved image. Must include path and format as well.
                i.e. '/Users/Paul/Desktop/bloch.png'
                This overrides the 'format' and 'dirc' arguments.
            output (str):
                Format of output image.
            dirc (str):
                Directory for output images. Defaults to current working directory.
        """
    self.render()
    if dirc:
        if not os.path.isdir(os.getcwd() + '/' + str(dirc)):
            os.makedirs(os.getcwd() + '/' + str(dirc))
    if name is None:
        if dirc:
            self.fig.savefig(os.getcwd() + '/' + str(dirc) + '/bloch_' + str(self.savenum) + '.' + output)
        else:
            self.fig.savefig(os.getcwd() + '/bloch_' + str(self.savenum) + '.' + output)
    else:
        self.fig.savefig(name)
    self.savenum += 1
    if self.fig:
        plt.close(self.fig)