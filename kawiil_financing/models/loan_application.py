from odoo import models, fields


class LoanApplication(models.Model):
    _name = 'loan.application'
    _description = 'Loan Application'

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
        required=True
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
    currency_field='currency_id'
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

   
