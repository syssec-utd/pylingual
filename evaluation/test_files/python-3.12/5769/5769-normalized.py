def generate(self, outputfile=None, dotfile=None, mapfile=None):
    """Generates a graph file.

        :param str outputfile: filename and path [defaults to graphname.png]
        :param str dotfile: filename and path [defaults to graphname.dot]
        :param str mapfile: filename and path

        :rtype: str
        :return: a path to the generated file
        """
    import subprocess
    name = self.graphname
    if not dotfile:
        if outputfile and outputfile.endswith('.dot'):
            dotfile = outputfile
        else:
            dotfile = '%s.dot' % name
    if outputfile is not None:
        storedir, _, target = target_info_from_filename(outputfile)
        if target != 'dot':
            pdot, dot_sourcepath = tempfile.mkstemp('.dot', name)
            os.close(pdot)
        else:
            dot_sourcepath = osp.join(storedir, dotfile)
    else:
        target = 'png'
        pdot, dot_sourcepath = tempfile.mkstemp('.dot', name)
        ppng, outputfile = tempfile.mkstemp('.png', name)
        os.close(pdot)
        os.close(ppng)
    pdot = codecs.open(dot_sourcepath, 'w', encoding='utf8')
    pdot.write(self.source)
    pdot.close()
    if target != 'dot':
        use_shell = sys.platform == 'win32'
        if mapfile:
            subprocess.call([self.renderer, '-Tcmapx', '-o', mapfile, '-T', target, dot_sourcepath, '-o', outputfile], shell=use_shell)
        else:
            subprocess.call([self.renderer, '-T', target, dot_sourcepath, '-o', outputfile], shell=use_shell)
        os.unlink(dot_sourcepath)
    return outputfile