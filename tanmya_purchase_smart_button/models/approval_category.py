import base64

from odoo import api, fields, models, tools, _

class ApprovalCategory(models.Model):
    _inherit = 'approval.category'

    manual_rfqs = fields.Boolean(string="Manual RFQ\'s")