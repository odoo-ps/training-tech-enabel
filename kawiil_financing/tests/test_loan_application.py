from pydoc import doc

from odoo import api
from odoo.tests.common import TransactionCase, tagged
from odoo.exceptions import ValidationError, UserError

@tagged('post_install', '-at_install')
class TestLoanApplication(TransactionCase):
    @api.model
    def _get_default_document_types(self):
        return self.env['loan.application.document.type'].search([])
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Création partenaire fictif
        cls.partner = cls.env['res.partner'].create({
            'name': 'Test Client'
        })

        #  Type document obligatoire
        cls.doc_type = cls.env['loan.application.document.type'].create({
            'name': 'Carte identité',
            'is_required': True

        })

    # TEST 1 : COMPUTE + CREATE
    def test_01_computes_and_crud(self):
        loan = self.env['loan.application'].create({
            'name': 'TEST-001',
            'partner_id': self.partner.id,
            'principal_amount': 10000,
            'down_payment': 2000,
            'interest_rate': 5,
        })

        #  Vérifier calcul
        self.assertEqual(loan.loan_amount, 8000)

        #  Créer un document lié
        self.env['loan.application.document'].create({
            'name': 'Doc Test',
            'loan_id': loan.id,
            'document_type_id': self.doc_type.id,
        })

        # Vérifier relation
        self.assertTrue(loan.document_ids)
        self.assertIn(doc, loan.document_ids)

    # TEST 2 : CONTRAINTES PYTHON

    def test_02_python_constraints(self):

        with self.assertRaises(ValidationError):
            self.env['loan.application'].create({
                'name': 'TEST-002',
                'partner_id': self.partner.id,
                'principal_amount': 5000,
                'down_payment': 5000,  # invalide
                'interest_rate': 5,
            })

    #  TEST 3 : WORKFLOW USER ERROR
    def test_03_workflow_user_error(self):

        loan = self.env['loan.application'].create({
            'name': 'TEST-003',
            'partner_id': self.partner.id,
            'principal_amount': 10000,
            'down_payment': 1000,
            'interest_rate': 5,
        })

        # documents non approuvés
        with self.assertRaises(UserError):
            loan.action_submit()

