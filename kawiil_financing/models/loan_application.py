from odoo import models, fields

class LoanApplication(models.Model):
    _name = 'loan.application'
    _description = 'Loan Application'

    name = fields.Char(
        string="Numéro de demande",
        required=True
    )

    partner_id = fields.Many2one(
        'res.partner',
        string="Client",
        required=True
    )

    user_id = fields.Many2one(
        'res.users',
        string="Vendeur",
        default=lambda self: self.env.user
    )

    product_id = fields.Many2one(
        'product.template',
        string="Moto"
    )

    currency_id = fields.Many2one(
        'res.currency',
        string="Devise",
        default=lambda self: self.env.company.currency_id
    )

    loan_amount = fields.Monetary(
        string="Montant du prêt",
        currency_field='currency_id',
        required=True
    )

    down_payment = fields.Monetary(
        string="Apport initial",
        currency_field='currency_id'
    )

    interest_rate = fields.Float(
        string="Taux d'intérêt",
        digits=(5, 2),
        required=True
    )

    loan_term = fields.Integer(
        string="Durée (Mois)",
        default=36
    )

    date_applied = fields.Date(
        string="Date de demande",
        default=fields.Date.today
    )

    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('sent', 'Envoyé'),
        ('credit_check', 'Vérification de solvabilité'),
        ('approved', 'Approuvé'),
        ('rejected', 'Rejeté'),
        ('signed', 'Signé'),
        ('cancelled', 'Annulé'),
    ],
        string="Statut",
        default='draft',
        copy=False
    )

    active = fields.Boolean(default=True)

    notes = fields.Html(
        string="Notes internes",
        copy=False
    )
