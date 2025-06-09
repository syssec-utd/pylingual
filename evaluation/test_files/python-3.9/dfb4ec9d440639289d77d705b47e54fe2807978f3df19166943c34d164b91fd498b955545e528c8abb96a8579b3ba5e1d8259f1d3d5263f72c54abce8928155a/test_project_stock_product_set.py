from odoo.tests import Form
from odoo.tests.common import users
from odoo.addons.project_stock.tests.common import TestProjectStockBase

class TestProjectStockProductSet(TestProjectStockBase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.task = cls._create_task(cls, [])
        cls.product_set = cls.env['product.set'].create({'name': 'Test product set', 'set_line_ids': [(0, 0, {'product_id': cls.product_a.id, 'quantity': 2}), (0, 0, {'product_id': cls.product_b.id, 'quantity': 1})]})

    @users('project-task-user')
    def test_wizard_product_set_add_1(self):
        self.assertFalse(self.task.move_ids)
        wizard_form = Form(self.env['product.set.add.from.task'].with_context(default_task_id=self.task.id))
        wizard_form.product_set_id = self.product_set
        wizard = wizard_form.save()
        wizard.add_set()
        self.assertTrue(self.task.group_id)
        self.assertEqual(len(self.task.move_ids), 2)
        self.assertIn(self.product_a, self.task.move_ids.mapped('product_id'))
        self.assertIn(self.product_b, self.task.move_ids.mapped('product_id'))
        self.assertEqual(sum(self.task.move_ids.mapped('product_uom_qty')), 3)

    @users('project-task-user')
    def test_wizard_product_set_add_2(self):
        task_form = Form(self.task)
        with task_form.move_ids.new() as move_form:
            move_form.product_id = self.product_c
            move_form.product_uom_qty = 1
        task_form.save()
        self.assertEqual(len(self.task.move_ids), 1)
        self.assertTrue(self.task.group_id)
        wizard_form = Form(self.env['product.set.add.from.task'].with_context(default_task_id=self.task.id))
        wizard_form.product_set_id = self.product_set
        wizard = wizard_form.save()
        wizard.add_set()
        self.assertTrue(self.task.group_id)
        self.assertEqual(len(self.task.move_ids), 3)
        self.assertIn(self.product_a, self.task.move_ids.mapped('product_id'))
        self.assertIn(self.product_b, self.task.move_ids.mapped('product_id'))
        self.assertEqual(sum(self.task.move_ids.mapped('product_uom_qty')), 4)
        self.task.action_confirm()
        self.assertEqual(len(self.task.move_ids), 3)
        move_a = self.task.move_ids.filtered(lambda x: x.product_id == self.product_a)
        self.assertEqual(move_a.group_id, self.task.group_id)
        move_b = self.task.move_ids.filtered(lambda x: x.product_id == self.product_b)
        self.assertEqual(move_b.group_id, self.task.group_id)
        move_c = self.task.move_ids.filtered(lambda x: x.product_id == self.product_c)
        self.assertEqual(move_c.group_id, self.task.group_id)