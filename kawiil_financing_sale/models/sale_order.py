from odoo import models, fields, api
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    loan_application_ids = fields.One2many(
        'loan.application',
        'sale_order_id',
        string="Prêts"
    )

    loan_count = fields.Integer(
        compute='_compute_loan_count'
    )

    def _compute_loan_count(self):
        for order in self:
            order.loan_count = len(order.loan_application_ids)

    # ✅ ACTION PRINCIPALE
    def action_create_loan(self):
        self.ensure_one()

        financeable_lines = self.order_line.filtered(
            lambda l: l.product_id.product_tmpl_id.is_financeable
        )

        # ✅ VALIDATION
        if not financeable_lines:
            raise UserError("Aucun produit finançable trouvé.")

        if len(financeable_lines) > 1:
            raise UserError("Une seule ligne finançable est autorisée.")

        line = financeable_lines[0]

        return {
            'name': self.env._("Créer une demande de prêt"),
            'type': 'ir.actions.act_window',
            'res_model': 'loan.application',
            'view_mode': 'form',
            'target': 'current',
            'context': {
                'default_sale_order_id': self.id,
                'default_partner_id': self.partner_id.id,
                'default_product_id': line.product_id.product_tmpl_id.id,
                'default_principal_amount': line.price_subtotal,
            }
        }

    # ✅ SMART BUTTON ACTION
    def action_view_loans(self):
        self.ensure_one()

        return {
            'name': self.env._("Prêts"),
            'type': 'ir.actions.act_window',
            'res_model': 'loan.application',
            'view_mode': 'list,form',
            'domain': [('sale_order_id', '=', self.id)],
            'context': {
                'default_sale_order_id': self.id
            }
        }
