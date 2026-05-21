from odoo import fields, models


class LoanApplication(models.Model):
    _inherit = "loan.application"

    sale_order_id = fields.Many2one(comodel_name="sale.order", string="Bon de commande")
