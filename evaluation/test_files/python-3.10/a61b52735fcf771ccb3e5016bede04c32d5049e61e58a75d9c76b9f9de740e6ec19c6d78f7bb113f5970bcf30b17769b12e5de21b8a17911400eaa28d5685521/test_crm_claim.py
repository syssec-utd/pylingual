from odoo.tests import common

class TestCrmClaim(common.TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(TestCrmClaim, cls).setUpClass()
        Claims = cls.env['crm.claim'].with_context(mail_create_nosubscribe=True)
        cls.claim = Claims.create({'name': 'Test Claim', 'team_id': cls.env.ref('sales_team.salesteam_website_sales').id})
        cls.partner = cls.env['res.partner'].create({'name': 'Partner Claim', 'email': 'partner.claim@example.com', 'phone': '1234567890'})
        cls.claim_categ = cls.env.ref('crm_claim.categ_claim1')
        cls.sales_team = cls.claim_categ.team_id

    def test_crm_claim(self):
        self.assertNotEqual(self.claim.team_id, self.sales_team)
        self.assertTrue(self.claim.stage_id.id)
        self.claim.partner_id = self.partner
        self.claim.onchange_partner_id()
        self.assertEqual(self.claim.email_from, self.partner.email)
        self.assertEqual(self.claim.partner_phone, self.partner.phone)
        self.assertEqual(self.partner.claim_count, 1)
        self.claim.categ_id = self.claim_categ
        self.claim.onchange_categ_id()
        self.assertEqual(self.claim.team_id, self.sales_team)
        new_claim = self.claim.copy()
        self.assertEqual(new_claim.stage_id.id, 1)
        self.assertIn('copy', new_claim.name)
        self.assertTrue(new_claim.stage_id.id)
        self.assertEqual(self.partner.claim_count, 2)