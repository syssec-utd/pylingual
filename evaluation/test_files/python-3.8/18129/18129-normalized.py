def _put_pages(self):
    """ First, the Document object does the heavy-lifting for the
            individual page objects and content.

            Then, the overall "Pages" object is generated.

        """
    self.document._get_orientation_changes()
    self.document._output_pages()
    self.session._add_object(1)
    self.session._out('<</Type /Pages')
    kids = '/Kids ['
    for i in xrange(0, len(self.document.pages)):
        kids += str(3 + 2 * i) + ' 0 R '
    self.session._out(kids + ']')
    self.session._out('/Count %s' % len(self.document.pages))
    self.session._out('/MediaBox [0 0 %.2f %.2f]' % (self.document.page.width, self.document.page.height))
    self.session._out('>>')
    self.session._out('endobj')