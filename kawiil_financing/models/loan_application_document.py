from odoo import fields, models


class LoanApplicationDocument(models.Model):
    _name = "loan.application.document"
    _description = "Loan Application Document"

    name = fields.Char(string="name", required=True)
    state = fields.Selection(
        selection=[
            ("new", "Nouveau"),
            ("approved", "Approuvé"),
            ("rejected", "Rejeté"),
        ],
    )
    type_id = fields.Many2one(comodel_name="loan.application.document.type", string="Type")
    application_id = fields.Many2one(comodel_name="loan.application", string="Demande de prêt")
    attachment_id = fields.Many2one(comodel_name="ir.attachment", string="Attachment")

