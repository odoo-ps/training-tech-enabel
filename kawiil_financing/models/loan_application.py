from odoo import fields, models


class LoanApplication(models.Model):
    _name = "loan.application"
    _description = "Loan Application"

    name = fields.Char(string="Numéro de demande", required=True)
    loan_term = fields.Integer(string="Durée (Mois)", default=36)
    interest_rate = fields.Float(string="Taux d'intérêt", digits=(5, 2))
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
    )
    active = fields.Boolean(default=True)
    notes = fields.Html(string="Notes internes")
