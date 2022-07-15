from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ApprovalRequest(models.Model):
    _inherit = 'approval.request'

    purchase_order_count_2 = fields.Integer(compute='_compute_purchase_order_count_2')
    manual_rfqs = fields.Boolean(related='category_id.manual_rfqs')

    def _compute_purchase_order_count_2(self):
        for request in self:
            related_purchase_order = self.env["purchase.order"].search([('approval_request_id', '=', request.id)])
            request.purchase_order_count_2 = len(related_purchase_order)

    def action_open_manually_created_orders(self):
        """ Return the list of purchase orders the approval request created or
        affected in quantity. """
        self.ensure_one()
        action = {
            'name': _('Manual RFQ\'s'),
            'view_type': 'tree',
            'view_mode': 'list,form',
            'res_model': 'purchase.order',
            'type': 'ir.actions.act_window',
            'domain': [('approval_request_id', '=', self.id)]
        }
        return action