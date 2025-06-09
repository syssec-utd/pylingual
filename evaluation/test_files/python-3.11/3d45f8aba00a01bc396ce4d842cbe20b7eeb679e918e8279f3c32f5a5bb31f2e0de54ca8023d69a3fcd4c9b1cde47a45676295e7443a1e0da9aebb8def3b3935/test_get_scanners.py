class GmpGetScannersTestMixin:

    def test_get_scanners(self):
        self.gmp.get_scanners()
        self.connection.send.has_been_called_with('<get_scanners/>')

    def test_get_scanners_with_filter_string(self):
        self.gmp.get_scanners(filter_string='foo=bar')
        self.connection.send.has_been_called_with('<get_scanners filter="foo=bar"/>')

    def test_get_scanners_with_filter_id(self):
        self.gmp.get_scanners(filter_id='f1')
        self.connection.send.has_been_called_with('<get_scanners filt_id="f1"/>')

    def test_get_scanners_with_trash(self):
        self.gmp.get_scanners(trash=True)
        self.connection.send.has_been_called_with('<get_scanners trash="1"/>')
        self.gmp.get_scanners(trash=False)
        self.connection.send.has_been_called_with('<get_scanners trash="0"/>')

    def test_get_scanners_with_details(self):
        self.gmp.get_scanners(details=True)
        self.connection.send.has_been_called_with('<get_scanners details="1"/>')
        self.gmp.get_scanners(details=False)
        self.connection.send.has_been_called_with('<get_scanners details="0"/>')