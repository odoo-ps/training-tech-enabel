from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # relation vers les prêts
    loan_application_ids = fields.One2many(
        'loan.application',
        'partner_id',
        string="Demandes de prêt"
    )

    #  compteur calculé
    loan_application_count = fields.Integer(
        compute='_compute_loan_application_count'
    )

    #  COMPUTE
    @api.depends('loan_application_ids')
    def _compute_loan_application_count(self):
        for partner in self:
            partner.loan_application_count = len(partner.loan_application_ids)


    # ACTION
    def action_view_loan_applications(self):
        self.ensure_one()

        return {
            'name': self.env._("Demandes de prêt"),
            'type': 'ir.actions.act_window',
            'res_model': 'loan.application',
            'view_mode': 'list,form',
            'domain': [('partner_id', '=', self.id)],
            'context': {
                'default_partner_id': self.id
            }
        }
