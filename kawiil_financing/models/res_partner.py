from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    loan_application_ids = fields.One2many(
        comodel_name='loan.application',
        inverse_name='partner_id',
        string='Loan Applications',
    )
    loan_application_count = fields.Integer(
        compute='_compute_loan_application_count',
    )

    def _compute_loan_application_count(self):
        data = self.env['loan.application'].read_group(
            domain=[('partner_id', 'in', self.ids)],
            fields=['partner_id'],
            groupby=['partner_id'],
        )
        counts = {row['partner_id'][0]: row['partner_id_count'] for row in data}
        for record in self:
            record.loan_application_count = counts.get(record.id, 0)

    def action_view_loan_applications(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': self.env._('Demandes de prêt'),
            'res_model': 'loan.application',
            'view_mode': 'list,form',
            'domain': [('partner_id', '=', self.id)],
            'context': {'default_partner_id': self.id},
        }
