from odoo import fields, models


class LoanApplicationTag(models.Model):
    _name = "loan.application.tag"
    _description = "Loan Application Tag"

    name = fields.Char(string="name")
    color = fields.Integer(string="color")