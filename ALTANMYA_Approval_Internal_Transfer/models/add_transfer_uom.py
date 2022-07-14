from odoo import api, fields, models, tools

class TransferUom(models.Model):
    _inherit = "product.template"


    @tools.ormcache()
    def _get_default_uom_id(self):
        # Deletion forbidden (at least through unlink)
        return self.env.ref('uom.product_uom_unit')

    uom_to_id = fields.Many2one(
        'uom.uom', 'Transfer UoM',
        default=_get_default_uom_id, required=True,
        help="Default unit of measure used for transfer orders. It must be in the same category as the default unit of measure.")


