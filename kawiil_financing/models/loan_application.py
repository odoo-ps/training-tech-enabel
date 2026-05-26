from odoo import _, models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.translate import _lt
from odoo.exceptions import UserError

_name_unique = models.Constraint(
    'UNIQUE(name)',
    _lt('Ce numéro de demande existe déjà.'),
)

_loan_amount_positive = models.Constraint(
    'CHECK(loan_amount > 0)',
    _lt('Le montant du capital doit être strictement supérieur à zéro.'),
)

class LoanApplication(models.Model):
    _name = 'loan.application'
    _description = 'Loan Application'

    def action_submit(self):
        for record in self:

            required_docs = record.document_ids.filtered(
                lambda d: d.type_id and d.type_id.is_required
            )

            if not required_docs:
                raise UserError(
                    record.env._("Aucun document obligatoire n'est fourni.")
                )

            not_approved = required_docs.filtered(lambda d: d.state != 'approved')

            if not_approved:
                raise UserError(
                    record.env._("Tous les documents obligatoires doivent être approuvés.")
                )

            record.state = 'sent'
            record.date_applied = fields.Date.today()

    def action_approve_loan(self):
        for record in self:
            record.state = 'approved'
            record.date_approved = fields.Date.today()

    def action_reject_loan(self):
        for record in self:
            record.state = 'rejected'
            record.date_rejected = fields.Date.today()

    name = fields.Char(string="Numéro de demande", required=True)
    #  CONSTRAINTS
   # _name_unique = models.Constraint(
     #   'UNIQUE(name)',
      #  _lt('Ce numéro de demande existe déjà.'),
   # )

    @api.constrains('principal_amount', 'down_payment')
    def _check_down_payment(self):
        for record in self:
            if record.down_payment >= record.principal_amount:
                raise ValidationError(
                    record.env._("L'apport doit être strictement inférieur au montant principal.")
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

    principal_amount = fields.Monetary(
        string="Montant principal",
        currency_field='currency_id',
        required=True
    )

    down_payment = fields.Monetary(
    string="Apport initial",
    currency_field='currency_id'
    )

    loan_amount = fields.Monetary(
        string="Montant du prêt",
        currency_field='currency_id',
        compute="_compute_loan_amount",
        inverse="_inverse_loan_amount",
        store=True
    )

    #  CALCUL
    @api.depends('principal_amount', 'down_payment')
    def _compute_loan_amount(self):
        for record in self:
            record.loan_amount = record.principal_amount - record.down_payment

    #  INVERSE
    def _inverse_loan_amount(self):
        for record in self:
            record.down_payment = record.principal_amount - record.loan_amount

    date_applied = fields.Date(
        string="Date de demande",
        default=fields.Date.today
    )

    active = fields.Boolean(default=True)

    #  AJOUT FINAL MANQUANT
    notes = fields.Html(
        string="Notes internes"
    )

    # CHAMPS LIEES

    email = fields.Char(
        related='partner_id.email',
        string="Email",
        readonly=True
    )

    phone = fields.Char(
        related='partner_id.phone',
        string="Téléphone",
        readonly=True
    )

    date_approved = fields.Date(
        string="Date d'approbation"
    )

    date_rejected = fields.Date(
        string="Date de rejet"
    )


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
        ('draft', 'Brouillon'),
        ('sent', 'Envoyé'),
        ('approved', 'Approuvé'),
        ('rejected', 'Rejeté'),
    ], default='draft')

    type_id = fields.Many2one('loan.application.document.type')
    application_id = fields.Many2one('loan.application', ondelete='cascade')
    attachment_id = fields.Many2one('ir.attachment')

    date_approved = fields.Date(string="Date d'approbation")
    date_rejected = fields.Date(string="Date de rejet")

    def action_approve_document(self):
        for record in self:
            record.state = 'approved'

    def action_reject_document(self):
        for record in self:
            record.state = 'rejected'

