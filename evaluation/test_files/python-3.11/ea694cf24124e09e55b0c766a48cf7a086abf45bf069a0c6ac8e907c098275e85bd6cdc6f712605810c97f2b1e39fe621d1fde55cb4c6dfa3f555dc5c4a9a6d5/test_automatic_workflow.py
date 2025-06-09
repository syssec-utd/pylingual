from datetime import datetime, timedelta
from odoo import fields
from .test_automatic_workflow_base import TestAutomaticWorkflowBase

class TestAutomaticWorkflow(TestAutomaticWorkflowBase):

    def test_full_automatic(self):
        workflow = self.create_full_automatic()
        sale = self.create_sale_order(workflow)
        sale._onchange_workflow_process_id()
        self.assertEqual(sale.state, 'draft')
        self.assertEqual(sale.workflow_process_id, workflow)
        self.progress()
        self.assertEqual(sale.state, 'sale')
        self.assertTrue(sale.picking_ids)
        self.assertTrue(sale.invoice_ids)
        invoice = sale.invoice_ids
        self.assertEqual(invoice.state, 'open')
        picking = sale.picking_ids
        self.progress()
        self.assertEqual(picking.state, 'done')

    def test_onchange(self):
        workflow = self.create_full_automatic()
        sale = self.create_sale_order(workflow)
        sale._onchange_workflow_process_id()
        self.assertEqual(sale.picking_policy, 'one')
        workflow2 = self.create_full_automatic(override={'picking_policy': 'direct'})
        sale.workflow_process_id = workflow2.id
        sale._onchange_workflow_process_id()
        self.assertEqual(sale.picking_policy, 'direct')

    def test_date_invoice_from_sale_order(self):
        workflow = self.create_full_automatic()
        last_week_time = datetime.now() - timedelta(days=7)
        last_week_time = fields.Datetime.to_string(last_week_time)
        last_week_date = last_week_time[:10]
        override = {'date_order': last_week_time}
        sale = self.create_sale_order(workflow, override=override)
        sale._onchange_workflow_process_id()
        self.assertEqual(sale.date_order, last_week_time)
        self.progress()
        self.assertTrue(sale.invoice_ids)
        invoice = sale.invoice_ids
        self.assertEqual(invoice.date_invoice, last_week_date)
        self.assertEqual(invoice.workflow_process_id, sale.workflow_process_id)

    def test_invoice_from_picking_with_service_product(self):
        workflow = self.create_full_automatic()
        product_service = self.env.ref('product.service_order_01')
        product_uom_hour = self.env.ref('product.product_uom_hour')
        override = {'order_line': [(0, 0, {'name': 'Prepaid Consulting', 'product_id': product_service.id, 'product_uom_qty': 1, 'product_uom': product_uom_hour.id})]}
        sale = self.create_sale_order(workflow, override=override)
        sale._onchange_workflow_process_id()
        self.progress()
        self.assertFalse(sale.picking_ids)
        self.assertTrue(sale.invoice_ids)
        invoice = sale.invoice_ids
        self.assertEqual(invoice.workflow_process_id, sale.workflow_process_id)

    def test_journal_on_invoice(self):
        sale_journal = self.env['account.journal'].search([('type', '=', 'sale')], limit=1)
        new_sale_journal = self.env['account.journal'].create({'name': 'TTSA', 'code': 'TTSA', 'type': 'sale'})
        workflow = self.create_full_automatic()
        sale = self.create_sale_order(workflow)
        sale._onchange_workflow_process_id()
        self.progress()
        self.assertTrue(sale.invoice_ids)
        invoice = sale.invoice_ids
        self.assertEqual(invoice.journal_id.id, sale_journal.id)
        workflow = self.create_full_automatic(override={'property_journal_id': new_sale_journal.id})
        sale = self.create_sale_order(workflow)
        sale._onchange_workflow_process_id()
        self.progress()
        self.assertTrue(sale.invoice_ids)
        invoice = sale.invoice_ids
        self.assertEqual(invoice.journal_id.id, new_sale_journal.id)