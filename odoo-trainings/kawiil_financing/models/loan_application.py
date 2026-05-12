from odoo import models, fields


class LoanApplication(models.Model):
    _name = 'loan.application'
    _description = 'Loan Application'

    name = fields.Char(required=True)
    loan_term =  fields.Integer(default=36)
    interest_rate = fields.Float(digits=(5,2))
    date_applied = fields.Date(default=lambda self:fields.Date.today())
    state = fields.Selection(selection=[('draft','draft'),('credit check','credit check')])
    active = fields.Boolean(default=True)
    notes = fields.Html()
    partner_id = fields.Many2one(comodel_name="res.partner")
    user_id = fields.Many2one(comodel_name="res.users")
    product_id = fields.Many2one(comodel_name="product.product")
    currency_id = fields.Many2one(comodel_name="res.currency")
    loan_amount = fields.Monetary(currency_field='currency_id')
    down_payment = fields.Monetary(currency_field='currency_id')