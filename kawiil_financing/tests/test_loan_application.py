from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError, ValidationError


class TestLoanApplication(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env['res.partner'].create({'name': 'Test Partner'})
        cls.doc_type = cls.env['loan.application.document.type'].create({
            'name': 'Identity Document',
            'is_required': True,
        })

    def test_01_computes_and_crud(self):
        loan = self.env['loan.application'].create({
            'name': 'TEST-001',
            'partner_id': self.partner.id,
            'principal_amount': 10000.0,
            'down_payment': 2000.0,
            'interest_rate': 5.0,
        })

        self.assertEqual(loan.loan_amount, 8000.0)
        self.assertTrue(loan.document_ids)

    def test_02_python_constraints(self):
        with self.assertRaises(ValidationError):
            self.env['loan.application'].create({
                'name': 'TEST-002',
                'partner_id': self.partner.id,
                'principal_amount': 5000.0,
                'down_payment': 10000.0,
                'interest_rate': 5.0,
            })

    def test_03_workflow_user_error(self):
        loan = self.env['loan.application'].create({
            'name': 'TEST-003',
            'partner_id': self.partner.id,
            'principal_amount': 10000.0,
            'down_payment': 2000.0,
            'interest_rate': 5.0,
        })

        with self.assertRaises(UserError):
            loan.action_submit()
