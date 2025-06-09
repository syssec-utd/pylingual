import mock
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
model = 'odoo.addons.base_report_to_printer.models.printing_server'

class StopTest(Exception):
    pass

class TestPrintingPrinterWizard(TransactionCase):

    def setUp(self):
        super(TestPrintingPrinterWizard, self).setUp()
        self.Model = self.env['printing.printer.update.wizard']
        self.server = self.env['printing.server'].create({})
        self.printer_vals = {'printer-info': 'Info', 'printer-make-and-model': 'Make and Model', 'printer-location': 'location', 'device-uri': 'URI', 'printer-uri-supported': 'uri'}

    def _record_vals(self, sys_name='sys_name'):
        return {'name': self.printer_vals['printer-info'], 'server_id': self.server.id, 'system_name': sys_name, 'model': self.printer_vals['printer-make-and-model'], 'location': self.printer_vals['printer-location'], 'uri': self.printer_vals['device-uri']}

    @mock.patch('%s.cups' % model)
    def test_action_ok_inits_connection(self, cups):
        """ It should initialize CUPS connection """
        self.Model.action_ok()
        cups.Connection.assert_called_once_with(host=self.server.address, port=self.server.port)

    @mock.patch('%s.cups' % model)
    def test_action_ok_gets_printers(self, cups):
        """ It should get printers from CUPS """
        cups.Connection().getPrinters.return_value = {'sys_name': self.printer_vals}
        cups.Connection().getPPD3.return_value = (200, 0, '')
        self.Model.action_ok()
        cups.Connection().getPrinters.assert_called_once_with()

    @mock.patch('%s.cups' % model)
    def test_action_ok_raises_warning_on_error(self, cups):
        """ It should raise Warning on any error """
        cups.Connection.side_effect = StopTest
        with self.assertRaises(UserError):
            self.Model.action_ok()

    @mock.patch('%s.cups' % model)
    def test_action_ok_creates_new_printer(self, cups):
        """ It should create new printer w/ proper vals """
        cups.Connection().getPrinters.return_value = {'sys_name': self.printer_vals}
        cups.Connection().getPPD3.return_value = (200, 0, '')
        self.Model.action_ok()
        rec_id = self.env['printing.printer'].search([('system_name', '=', 'sys_name')], limit=1)
        self.assertTrue(rec_id)
        for (key, val) in self._record_vals().items():
            if rec_id._fields[key].type == 'many2one':
                val = self.env[rec_id._fields[key].comodel_name].browse(val)
            self.assertEqual(val, rec_id[key])

    @mock.patch('%s.cups' % model)
    def test_action_ok_skips_existing_printer(self, cups):
        """ It should not recreate existing printers """
        cups.Connection().getPrinters.return_value = {'sys_name': self.printer_vals}
        cups.Connection().getPPD3.return_value = (200, 0, '')
        self.env['printing.printer'].create(self._record_vals())
        self.Model.action_ok()
        res_ids = self.env['printing.printer'].search([('system_name', '=', 'sys_name')])
        self.assertEqual(1, len(res_ids))