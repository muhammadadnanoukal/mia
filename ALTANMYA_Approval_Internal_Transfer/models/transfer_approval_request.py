from odoo import api, fields, models, _
from odoo.exceptions import UserError



class ApprovalRequest(models.Model):
    _inherit = 'approval.request'

    transfer_order_count = fields.Integer(compute='_compute_transfer_order_count')

    trans_type = fields.Many2one(related='category_id.transfer_type')

    location_id = fields.Many2one(
        'stock.location', 'Source Location',
        auto_join=True, index=True,
        check_company=True,
        help="Sets a location if you produce at a fixed location. This can be "
             "a partner location if you subcontract the manufacturing operations.")

    location_dest_id = fields.Many2one(
        'stock.location', 'Destination Location',
        auto_join=True, index=True,
        check_company=True,
        help="Location where the system will stock the finished products.")


    @api.depends('product_line_ids.transfer_order_line_id')
    def _compute_transfer_order_count(self):
        for request in self:
            transfers = request.product_line_ids.transfer_order_line_id.picking_id
            request.transfer_order_count = len(transfers)

    def action_approve(self, approver=None):
        if self.approval_type == 'transfer' and any(not line.product_id for line in self.product_line_ids):
            raise UserError(_("You must select a product for each line of requested products."))
        return super().action_approve(approver)

    def action_cancel(self):
        """ Override to notify Transfer Orders when the Approval Request is cancelled. """
        res = super().action_cancel()
        transfers = self.product_line_ids.transfer_order_line_id.move_id
        for transfer in transfers:
            product_lines = self.product_line_ids.filtered(
                lambda line: line.transfer_order_line_id.move_id.id == transfer.id
            )
        return res

    def action_confirm(self):
        for request in self:
            if request.approval_type == 'transfer' and not request.product_line_ids:
                raise UserError(_("You cannot create an empty transfer request."))
        return super().action_confirm()

    def get_transfer_type_id(self):
        tr_type_name = self.trans_type.name
        tr_type_id = self.env['stock.picking.type'].search([('name', '=', tr_type_name)], limit=1).id
        return tr_type_id

    def _get_picking_values(self):
        tr_type_id = self.get_transfer_type_id()
        return {
            'name' : self.name,
            'user_id' : self.request_owner_id.id,
            'state' : 'assigned',
            'company_id' : self.company_id.id,
            'move_type' : 'direct',
            'partner_id': self.location_id.id,
            'location_id' : self.location_id.id,
            'location_dest_id' : self.location_dest_id.id,
            'picking_type_id': tr_type_id,
        }

    def action_create_transfer_orders(self):
        self.ensure_one()

        picking_line = self._get_picking_values()
        picking_record = self.env['stock.picking'].sudo().create(picking_line)

        for line in self.product_line_ids:

            to_vals = line._get_transfer_order_values()
            new_transfer_order = self.env['stock.move'].create(dict(to_vals,location_id = self.location_id.id
                                                                    ,location_dest_id = self.location_dest_id.id
                                                                    ,picking_id = picking_record.id
                                                                    ,product_uom_qty = line.quantity))
            transfer_order_line_vals = self.env['stock.move.line']._prepare_transfer_line_vals(
                line.product_id,
                None,
                line.product_uom_id,
                line.company_id,
                new_transfer_order,
            )
            new_to_line = self.env['stock.move.line'].create(dict(transfer_order_line_vals
                                                                  ,picking_id = picking_record.id))
            line.transfer_order_line_id = new_to_line.id
            new_transfer_order.move_line_ids = [(4, new_to_line.id)]

            new_transfer_order.reference = self.name

    def action_open_transfer_orders(self):
        """ Return the list of transfer orders the approval request created or
        affected in quantity. """
        self.ensure_one()
        transfer_ids = self.product_line_ids.transfer_order_line_id.picking_id.ids
        domain = [('id', 'in', transfer_ids)]
        action = {
            'name': _('Transfer Orders'),
            'view_type': 'tree',
            'view_mode': 'list,form',
            'res_model': 'stock.picking',
            'type': 'ir.actions.act_window',
            'context': self.env.context,
            'domain': domain,
        }
        return action