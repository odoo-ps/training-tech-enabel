from odoo.exceptions import UserError, ValidationError
from odoo.tests import TransactionCase


class TestLoanApplication(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create({
            "name": "Test Partner",
        })
        cls.document_type = cls.env["loan.application.document.type"].create({
            "name": "dummy test type",
            "is_mandatory": True,
        })

    def test_01_computes_and_crud(self):
        application = self.env["loan.application"].create({
            "name": "TEST-001",
            "partner_id": self.partner.id,
            "loan_amount": 10000,
            "down_payment": 2000,
            "interest_rate": 0,
        })
        self.assertEqual(application.total_loan_amount, 9000)
        self.assertTrue(application.document_ids)


    def test_02_python_constraints(self):
        with self.assertRaises(ValidationError):
            self.env["loan.application"].create({
                "name": "TEST-002",
                "partner_id": self.partner.id,
                "loan_amount": 5000,
                "down_payment": 10000,
                "interest_rate": 0,
            })


    def test_03_workflow_user_error(self):
        application = self.env["loan.application"].create({
            "name": "TEST-003",
            "partner_id": self.partner.id,
            "loan_amount": 10000,
            "down_payment": 2000,
            "interest_rate": 0,
        })
        with self.assertRaises(UserError):
            application.action_submit()


    def test_04_workflow_valid_ok(self):
        application = self.env["loan.application"].create({
            "name": "TEST-004",
            "partner_id": self.partner.id,
            "loan_amount": 10000,
            "down_payment": 2000,
            "interest_rate": 0,
        })
        application.document_ids.filtered(
            lambda d: d.type_id.is_mandatory
        ).write({"state": "approved"})
        application.action_submit()
        self.assertEqual(application.state, "sent")