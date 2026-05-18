from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class LoanApplication(models.Model):
    _name = 'loan.application'
    _description = 'Loan Application'

    _name_uniq = models.Constraint(
        'unique(name)',
        'A tag with the same name already exists in this country.',
    )

    _principal_amount_positive_check = models.Constraint(
        "CHECK(principal_amount >= 0)",
        "The principal amount must be a positive value.",
    )


    name = fields.Char(string="Numéro de demande", required=True)

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

    loan_amount = fields.Monetary(
        string="Montant du prêt",
        compute='_compute_loan_amount',
        inverse='_inverse_loan_amount',
        store=True,
        currency_field='currency_id'
    )

    currency_id = fields.Many2one(
        'res.currency',
        default=lambda self: self.env.company.currency_id
    )

    interest_rate = fields.Float(
        string="Taux d'intérêt",
        required=True
    )

    loan_term = fields.Integer(default=36)

    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('approved', 'Approuvé'),
        ('rejected', 'Rejeté')
    ], default='draft')

    #  NOUVEAUX CHAMPS
    tag_ids = fields.Many2many(
        'loan.application.tag',
        string="Tags"
    )

    document_ids = fields.One2many(
        'loan.application.document',
        'application_id',
        string="Documents"
    )

    product_id = fields.Many2one(
        'product.template',
        string="Produit"
    )

    down_payment = fields.Monetary(
        string="Apport initial",
        currency_field='currency_id',
        default=0.0
    )

    date_applied = fields.Date(
        string="Date de demande",
        default=fields.Date.today
    )

    active = fields.Boolean(default=True)

    #  AJOUT FINAL MANQUANT
    notes = fields.Html(
        string="Notes internes"
    )

    customer_email = fields.Char(related='partner_id.email')
    customer_phone = fields.Char(related='partner_id.phone')
    principal_amount = fields.Monetary(
        string="Montant principal",
        currency_field='currency_id',
        required=True
    )

    @api.constrains('principal_amount', 'down_payment')
    def _check_amounts(self):
        for rec in self:
            if rec.down_payment >= rec.principal_amount:
                raise ValidationError(_("The initial payment should be less than the total amount."))

    @api.depends('principal_amount', 'down_payment')
    def _compute_loan_amount(self):
        for rec in self:
            rec.loan_amount = (rec.principal_amount or 0.0) - (rec.down_payment or 0.0)

    def _inverse_loan_amount(self):
        for rec in self:
            rec.down_payment = (rec.principal_amount or 0.0) - (rec.loan_amount or 0.0)


#  TAGS
class LoanApplicationTag(models.Model):
    _name = 'loan.application.tag'
    _description = 'Loan Application Tag'

    name = fields.Char(required=True)
    color = fields.Integer()


#  DOCUMENT TYPE
class LoanApplicationDocumentType(models.Model):
    _name = 'loan.application.document.type'
    _description = 'Loan Application Document Type'

    name = fields.Char(required=True)
    is_required = fields.Boolean(string="Obligatoire")
    active = fields.Boolean(default=True)


#  DOCUMENT
class LoanApplicationDocument(models.Model):
    _name = 'loan.application.document'
    _description = 'Loan Application Document'

    name = fields.Char(required=True)

    state = fields.Selection([
        ('new', 'Nouveau'),
        ('approved', 'Approuvé'),
        ('rejected', 'Rejeté'),
    ], default='new')

    type_id = fields.Many2one('loan.application.document.type')
    application_id = fields.Many2one('loan.application', ondelete='cascade')
    attachment_id = fields.Many2one('ir.attachment')


