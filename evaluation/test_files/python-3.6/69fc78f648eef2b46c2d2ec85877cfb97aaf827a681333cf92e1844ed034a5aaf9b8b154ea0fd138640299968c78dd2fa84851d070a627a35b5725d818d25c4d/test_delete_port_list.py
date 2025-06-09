from gvm.errors import GvmError

class GmpDeletePortListTestMixin:

    def test_delete(self):
        self.gmp.delete_port_list('a1')
        self.connection.send.has_been_called_with('<delete_port_list port_list_id="a1" ultimate="0"/>')

    def test_delete_ultimate(self):
        self.gmp.delete_port_list('a1', ultimate=True)
        self.connection.send.has_been_called_with('<delete_port_list port_list_id="a1" ultimate="1"/>')

    def test_missing_id(self):
        with self.assertRaises(GvmError):
            self.gmp.delete_port_list(None)
        with self.assertRaises(GvmError):
            self.gmp.delete_port_list('')