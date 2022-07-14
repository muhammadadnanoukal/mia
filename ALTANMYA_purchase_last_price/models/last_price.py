from odoo import api, fields, models, _

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    _description = 'Purchase Order Line, Product Last Price'

    last_price = fields.Float(string='Last Price')

    @api.onchange('product_id')
    def _onchange_last_price(self):
        if self.product_id.id:
            self._cr.execute(
                'SELECT price FROM product_supplierinfo WHERE product_tmpl_id = {} ORDER BY id DESC LIMIT 1'.format(
                    self.product_id.id)
            )
            _res = self._cr.dictfetchall()
            if _res is not None and len(_res) != 0:
                self.last_price = _res[0].get('price')
            else:
                self.last_price = 0