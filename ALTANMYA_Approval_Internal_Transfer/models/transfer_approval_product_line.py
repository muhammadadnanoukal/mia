from odoo import api, fields, models, _
from odoo.exceptions import UserError
import datetime


class TanmyaApprovalProductLine(models.Model):
    _inherit = 'approval.product.line'

    def _domain_product_id(self):
        """ Filters on product to get only the ones who are available on
        transfer in the case the approval request type is transfer. """
        if 'default_category_id' in self.env.context:
            category_id = self.env.context.get('default_category_id')
        elif self.env.context.get('active_model') == 'approval.category':
            category_id = self.env.context.get('active_id')
        else:
            return []
        category = self.env['approval.category'].browse(category_id)
        if category.approval_type == 'transfer':
            return [('transfer_ok', '=', True)]

    # to => transfer order
    to_uom_qty = fields.Float(
        "Transfer UoM Quantity", compute='_compute_to_uom_qty',
        help="The quantity converted into the UoM used by the product in Transfer Order.")
    transfer_order_line_id = fields.Many2one('stock.move.line')
    product_id = fields.Many2one(domain=lambda self: self._domain_product_id())

    @api.depends('approval_request_id.approval_type', 'product_uom_id', 'quantity')
    def _compute_to_uom_qty(self):
        for line in self:
            approval_type = line.approval_request_id.approval_type
            if approval_type == 'transfer' and line.product_id and line.quantity:
                uom = line.product_uom_id or line.product_id.uom_id
                line.to_uom_qty = uom._compute_quantity(line.quantity, line.product_id.uom_to_id)
            else:
                line.to_uom_qty = 0.0

    def _get_transfer_orders_domain(self):
        """ Return a domain to get transfer order(s) where this product line could fit in.
        :return: list of tuple.
        """
        self.ensure_one()
        domain = [('company_id', '=', self.company_id.id),
                  ('state', '=', 'draft'),]
        return domain

    def _get_transfer_order_values(self):
        """ Get some values used to create a transfer order.
        Called in approval.request `action_create_transfer_orders`.
        :return: dict of values
        """
        self.ensure_one()
        vals = {
                'name' : self.product_id.name,
                'company_id': self.company_id.id,
                'product_id': self.product_id.id,
                'product_uom': self.product_uom_id.id,
        }
        return vals
