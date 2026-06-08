from odoo import models, fields


class LoanApplication(models.Model):
    _inherit = 'loan.application'

    sale_order_id = fields.Many2one(
        'sale.order',
        string="Commande"
    )
