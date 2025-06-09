def buildcontainer(self):
    """generate HTML div"""
    if self.container:
        return
    if self.width:
        if self.width[-1] != '%':
            self.style += 'width:%spx;' % self.width
        else:
            self.style += 'width:%s;' % self.width
    if self.height:
        if self.height[-1] != '%':
            self.style += 'height:%spx;' % self.height
        else:
            self.style += 'height:%s;' % self.height
    if self.style:
        self.style = 'style="%s"' % self.style
    self.container = self.containerheader + '<div id="%s"><svg %s></svg></div>\n' % (self.name, self.style)