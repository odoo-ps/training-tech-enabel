from odoo import fields, models


class LoanApplication(models.Model):
    _name = "loan.application"
    _description = "Loan Application"

    name = fields.Char(string="Numéro de demande", required=True)
    loan_term = fields.Integer(string="Durée (Mois)", default=36)
    interest_rate = fields.Float(string="Taux d'intérêt", digits=(5, 2), required=True)
    date_applied = fields.Date(
        string="Date de demande",
        default=lambda self: fields.Date.today(),
    )
    state = fields.Selection(
        selection=[
            ("draft", "Brouillon"),
            ("sent", "Envoyé"),
            ("solvency_check", "Vérification de solvabilité"),
            ("approved", "Approuvé"),
            ("rejected", "Rejeté"),
            ("signed", "Signé"),
            ("cancelled", "Annulé"),
        ],
        default="draft",
        copy=False
    )
    active = fields.Boolean(default=True)
    notes = fields.Html(string="Notes internes", copy=False)

    partner_id = fields.Many2one(comodel_name="res.partner", string="Client", required=True)
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Vendeur",
        default=lambda self: self.env.user,
    )
    product_id = fields.Many2one(comodel_name="product.template", string="Moto")

    currency_id = fields.Many2one(comodel_name="res.currency")
    loan_amount = fields.Monetary(string="Montant du prêt", currency_field="currency_id", required=True)
    down_payment = fields.Monetary(string="Acompte", currency_field="currency_id")

    tag_ids = fields.Many2many(comodel_name="loan.application.tag")
    document_ids = fields.One2many(
        comodel_name="loan.application.document",
        inverse_name="application_id",
    )
