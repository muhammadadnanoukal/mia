from odoo import api, fields, models, tools
from datetime import date, datetime,timedelta



class PurchaseSmartButton(models.Model):
    _inherit = 'purchase.order'

    approval_request_id = fields.Many2one('approval.request',string="Related Approval" ,required=False, domain="[('category_id.name', 'ilike', 'Create RFQ')]")
