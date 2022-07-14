from odoo import api, fields, models, _

CATEGORY_SELECTION = [
    ('required', 'Required'),
    ('optional', 'Optional'),
    ('no', 'None')]


class TanmyaApproval(models.Model):
    _inherit = 'approval.category'

    approval_type = fields.Selection(selection_add=[('transfer', 'Create Transfer Request')])

    def _default_transfer_type(self):
        return self.env['stock.picking.type'].search([('name', '=', 'Receipts')], limit=1)

    transfer_type = fields.Many2one('stock.picking.type', 'Operation Type',
                                    default=_default_transfer_type,
                                    ondelete="cascade")

    has_product = fields.Selection(
        CATEGORY_SELECTION, string="Has Product", default="required", required=True,
        help="Additional products that should be specified on the request.")

    has_quantity = fields.Selection(CATEGORY_SELECTION, string="Has Quantity", default="required", required=True)

    # Override this method from approval.category to
    # add default src & dest locations
    def create_request(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "approval.request",
            "views": [[False, "form"]],
            "context": {
                'form_view_initial_mode': 'edit',
                'default_name': _('New') if self.automated_sequence else self.name,
                'default_category_id': self.id,
                # assign deafault locations of operation type to src & dest in approval request
                'default_location_id': self.transfer_type.default_location_src_id.id,
                'default_location_dest_id': self.transfer_type.default_location_dest_id.id,
                ###############################################################################
                'default_request_owner_id': self.env.user.id,
                'default_request_status': 'new'
            },
        }