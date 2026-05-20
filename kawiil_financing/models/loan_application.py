from odoo import Command, _, api, fields, models
from odoo.tools.translate import _lt
from odoo.exceptions import UserError, ValidationError


class LoanApplication(models.Model):
    _name = "loan.application"
    _inherit = ['mail.thread', 'mail.activity.mixin']
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
        copy=False,
        tracking=True
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
    loan_amount = fields.Monetary(string="Montant du prêt", currency_field="currency_id", required=True, tracking=True)
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

    _name_unique = models.Constraint(
        'UNIQUE(name)',
        _lt('Ce numéro de demande existe déjà.'),
    )

    _loan_amount_positive = models.Constraint(
        'CHECK(loan_amount > 0)',
        _lt('Le montant du capital doit être strictement supérieur à zéro.'),
    )
    date_approved = fields.Date(string="Date d'approbation")
    date_rejected = fields.Date(string="Date de rejet")

    @api.model
    def _get_default_document_types(self):
        return self.env["loan.application.document.type"].search([('is_mandatory', '=', True)])

    @api.model_create_multi
    def create(self, vals_list):
        document_types = self._get_default_document_types()
        for vals in vals_list:
            vals["document_ids"] = vals.get("document_ids", []) + [
                Command.create({
                    "name": doc_type.name,
                    "type_id": doc_type.id
                }) for doc_type in document_types
            ]
        return super().create(vals_list)

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


    def action_submit(self):
        mandatory_docs = self.document_ids.filtered(lambda d: d.type_id.is_mandatory)
        if not mandatory_docs or any(d.state != "approved" for d in mandatory_docs):
            raise UserError(self.env._("Tous les documents obligatoires doivent être approuvés avant la soumission."))
        self.state = "sent"
        self.date_applied = fields.Date.today()
        self.message_post(
            body=self.env._("Demande soumise avec succès pour révision !"),
            subtype_xmlid="mail.mt_note",
        )

    def action_approve_loan(self):
        self.state = "approved"
        self.date_approved = fields.Date.today()

    def action_reject_loan(self):
        self.state = "rejected"
        self.date_rejected = fields.Date.today()