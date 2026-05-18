from odoo import _, api, fields, models
from odoo.tools.translate import _lt
from odoo.exceptions import ValidationError


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
    partner_email = fields.Char(related="partner_id.email")
    partner_phone = fields.Char(related="partner_id.phone")
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Vendeur",
        default=lambda self: self.env.user,
    )
    product_id = fields.Many2one(comodel_name="product.template", string="Moto")

    currency_id = fields.Many2one(comodel_name="res.currency")
    loan_amount = fields.Monetary(string="Montant du prêt", currency_field="currency_id", required=True)
    down_payment = fields.Monetary(string="Acompte", currency_field="currency_id")
    total_loan_amount = fields.Monetary(
        string="Montant total du prêt",
        currency_field="currency_id",
        compute="_compute_total_loan_amount",
        store=True,
    )

    tag_ids = fields.Many2many(comodel_name="loan.application.tag")
    document_ids = fields.One2many(
        comodel_name="loan.application.document",
        inverse_name="application_id",
    )

    _sql_constraints = [
        ("name_unique", "UNIQUE(name)", _lt("Ce numéro de demande existe déjà.")),
        ("loan_amount_positive", "CHECK(loan_amount > 0)", _lt("Le montant du capital doit être strictement supérieur à zéro.")),
    ]

    @api.depends("loan_amount", "down_payment", "interest_rate")
    def _compute_total_loan_amount(self):
        for record in self:
            net_capital = record.loan_amount - record.down_payment
            record.total_loan_amount = net_capital * (1 + record.interest_rate / 100)



    @api.constrains("down_payment", "loan_amount")
    def _check_down_payment(self):
        for record in self:
            if record.down_payment >= record.loan_amount:
                raise ValidationError(_("l'apport ne peut être supérieure ou égal au prêt"))
