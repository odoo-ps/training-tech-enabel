# test_capstone.py
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo import Command

class TestSalesBridge(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Create a Financeable Product (Motorcycle)
        cls.product_motorcycle = cls.env['product.product'].create({
            'name': 'Test Motorcycle',
            'is_financeable': True,
            'list_price': 15000.0,
        })
        # Create a Non-Financeable Product (Helmet)
        cls.product_helmet = cls.env['product.product'].create({
            'name': 'Test Helmet',
            'is_financeable': False,
            'list_price': 500.0,
        })
        cls.partner = cls.env['res.partner'].create({'name': 'Test Rider'})

    def test_01_create_loan_action(self):
        """ Test that the 'Create Loan' button returns the correct window action context. """
        # Create a Sale Order with one motorcycle
        order = self.env['sale.order'].create({
            'partner_id': self.partner.id,
            'order_line': [Command.create({'product_id': self.product_motorcycle.id})]
        })
        
        # Trigger the action (this method doesn't exist yet, you must build it!)
        action = order.action_create_loan()
        
        # Assertions: Verify it opens the correct view
        self.assertEqual(action['type'], 'ir.actions.act_window')
        self.assertEqual(action['res_model'], 'loan.application')
        
        # Verify Context Pre-fill: Did the data carry over?
        context = action['context']
        self.assertEqual(context.get('default_sale_order_id'), order.id, "Context missing default_sale_order_id")
        self.assertEqual(context.get('default_partner_id'), self.partner.id, "Context missing default_partner_id")
        self.assertEqual(context.get('default_product_id'), self.product_motorcycle.id, "Context missing default_product_id")
        self.assertEqual(context.get('default_principal_amount'), 15000.0, "Context missing default_principal_amount")

    def test_02_mvp_constraint(self):
        """ Test that the system blocks loans for orders with 2 motorcycles. """
        order = self.env['sale.order'].create({
            'partner_id': self.partner.id,
            'order_line': [
                Command.create({'product_id': self.product_motorcycle.id}),
                Command.create({'product_id': self.product_motorcycle.id}), # Second bike
            ]
        })
        
        # The system should raise a UserError to prevent complex loans (MVP Constraint)
        with self.assertRaises(UserError):
            order.action_create_loan()

    def test_03_non_financeable_blocker(self):
        """ Test that the system blocks loans for orders with no financeable products. """
        order = self.env['sale.order'].create({
            'partner_id': self.partner.id,
            'order_line': [Command.create({'product_id': self.product_helmet.id})]
        })
        
        with self.assertRaises(UserError):
            order.action_create_loan()
            