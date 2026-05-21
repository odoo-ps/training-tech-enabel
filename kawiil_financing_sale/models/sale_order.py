from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    loan_application_ids = fields.One2many(
        comodel_name="loan.application",
        inverse_name="sale_order_id",
        string="Demandes de prêt",
    )
    loan_application_count = fields.Integer(compute="_compute_loan_application_count")

    @api.depends("loan_application_ids")
    def _compute_loan_application_count(self):
        data = self.env["loan.application"].read_group(
            domain=[("sale_order_id", "in", self.ids)],
            fields=["sale_order_id"],
            groupby=["sale_order_id"],
        )
        counts = {row["sale_order_id"][0]: row["sale_order_id_count"] for row in data}
        for record in self:
            record.loan_application_count = counts.get(record.id, 0)

    def action_view_loan_applications(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Demandes de prêt"),
            "res_model": "loan.application",
            "view_mode": "list,form",
            "domain": [("sale_order_id", "=", self.id)],
            "context": {"default_sale_order_id": self.id},
        }

    def action_create_loan(self):
        financeable_lines = self.order_line.filtered(
            lambda line: line.product_id.is_financeable
        )
        if not financeable_lines:
            raise UserError(_("Aucun produit finançable trouvé dans les lignes de commande."))
        if len(financeable_lines) > 1:
            raise UserError(_("Plusieurs produits finançables trouvés. Une seule demande de prêt peut être créée par commande."))

        line = financeable_lines[0]
        return {
            "type": "ir.actions.act_window",
            "name": _("Nouvelle demande de prêt"),
            "res_model": "loan.application",
            "view_mode": "form",
            "target": "current",
            "context": {
                "default_sale_order_id": self.id,
                "default_partner_id": self.partner_id.id,
                "default_product_id": line.product_id.id,
                "default_principal_amount": line.price_subtotal,
            },
        }
