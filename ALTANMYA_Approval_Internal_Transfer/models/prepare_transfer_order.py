from datetime import datetime, time
from dateutil.relativedelta import relativedelta
from functools import partial
from itertools import groupby
import json

from markupsafe import escape, Markup
from pytz import timezone, UTC
from werkzeug.urls import url_encode

from odoo import api, fields, models, _
from odoo.osv import expression
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_compare, float_is_zero, float_round
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools.misc import formatLang, get_lang, format_amount

class PrepareTransferOrder(models.Model):
    _inherit = "stock.move.line"

    def _prepare_transfer_line_vals(self, product_id, product_qty, product_uom, company_id, tr_order, reserved_quant=None):
        vals = {
            'move_id': tr_order.id,
            'product_uom_qty' : product_qty,
            'product_id': product_id.id,
            'product_uom_id': product_uom.id,
            'location_id': tr_order.location_id.id,
            'picking_id': tr_order.picking_id.id,
            'company_id': company_id.id,
        }

        package = None

        if reserved_quant:
            package = reserved_quant.package_id
            vals = dict(
                vals,
                location_id=reserved_quant.location_id.id,
                lot_id=reserved_quant.lot_id.id or False,
                package_id=package.id or False,
                owner_id =reserved_quant.owner_id.id or False,
            )

        # apply putaway
        # , packaging=tr_order.product_packaging_id
        # location_dest_id = tr_order.location_dest_id._get_putaway_strategy(product_id, quantity=product_qty or 0, package=package).id
        # vals['location_dest_id'] = location_dest_id

        vals['location_dest_id'] = tr_order.location_dest_id.id


        return vals
