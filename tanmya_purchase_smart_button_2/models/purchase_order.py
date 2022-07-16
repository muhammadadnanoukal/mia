from odoo import api, fields, models, tools
from datetime import date, datetime,timedelta



class PurchaseSmartButton(models.Model):
    _inherit = 'purchase.order'

    approval_request_id = fields.Many2one('approval.request',string="Related Approval" ,required=False, domain="[('category_id.name', 'ilike', 'Create RFQ')]")

    @api.model
    def create(self, vals):
        if self.env.context.get('related_approval_request'):
            vals.update({'approval_request_id': self.env.context.get('related_approval_request')})
        return super().create(vals)

