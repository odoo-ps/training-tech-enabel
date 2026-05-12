from odoo import models, fields


class LoanApplication(models.Model):
    _name = "loan.application"
    _description = "Loan Application"

    # ---- Relations ----
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Client",
        required=True
    )

    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Vendeur",
        default=lambda self: self.env.user
    )

    product_id = fields.Many2one(
        comodel_name="product.template",
        string="Moto"
    )

    # ---- Montants & devise ----
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Devise",
        default=lambda self: self.env.company.currency_id
    )

    loan_amount = fields.Monetary(
        string="Montant du prêt",
        currency_field="currency_id"
    )

    down_payment = fields.Monetary(
        string="Apport initial",
        currency_field="currency_id"
    )

    # ---- Champs métiers ----
    name = fields.Char(string="Numéro de demande", required=True)
    loan_term = fields.Integer(string="Durée (Mois)", default=36)
    interest_rate = fields.Float(string="Taux d'intérêt", digits=(5, 2))
    date_applied = fields.Date(
        string="Date de demande",
        default=lambda self: fields.Date.today()
    )

    state = fields.Selection(
        [
            ("draft", "Brouillon"),
            ("sent", "Envoyé"),
            ("credit_check", "Vérification de solvabilité"),
            ("approved", "Approuvé"),
            ("rejected", "Rejeté"),
            ("signed", "Signé"),
            ("cancelled", "Annulé"),
        ],
        string="Statut",
        default="draft",
    )

    active = fields.Boolean(default=True)
    notes = fields.Html(string="Notes internes")
