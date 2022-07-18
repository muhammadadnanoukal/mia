from odoo import api, fields, models



class AccountMove(models.Model):
    _inherit = "account.move"

    total_after_discount = fields.Monetary(string='Total After Discount',
                                           compute='_compute_total_after_discount', store=True)

    total_after_discount_taxes = fields.Monetary(string='Total After Taxes & Discount',
                                           compute='_compute_total_after_discount', store=True)


    @api.depends('line_ids')
    def _compute_total_after_discount(self):
        for rec in self:
            rec.total_after_discount = 0.0
            rec.total_after_discount_taxes = 0.0
            for line in rec.line_ids:
                if line.product_id:
                    rec.total_after_discount += line.subtotal_after_discount
                    rec.total_after_discount_taxes += (line.subtotal_after_discount + line._get_taxes_line_amount())


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    discount_percent = fields.Float(string='Disc Percent')
    discount_amount = fields.Float(string='Disc Amount')

    subtotal_after_discount = fields.Monetary(string='Subtotal After Discount',
                                              compute='_compute_subtotal_after_discount', store=True)


    def _get_taxes_line_amount(self):
        total_taxes_amount = 0.0
        for tax in self.tax_ids:
            tax_amount = (tax.amount * self.price_unit) / 100
            total_taxes_amount += tax_amount
        return total_taxes_amount


    @api.depends('discount_percent','discount_amount','price_unit')
    def _compute_subtotal_after_discount(self):
        for rec in self:
            rec.subtotal_after_discount = rec.price_unit

            if rec.discount_percent > 0 and rec.discount_amount > 0:

                percent_amount = (rec.price_unit * rec.discount_percent) / 100
                temp_subtotal = rec.price_unit - percent_amount
                rec.subtotal_after_discount = temp_subtotal - rec.discount_amount

            elif rec.discount_amount > 0:
                rec.subtotal_after_discount = rec.price_unit - rec.discount_amount

            elif rec.discount_percent > 0:
                percent_amount = (rec.price_unit * rec.discount_percent) / 100
                rec.subtotal_after_discount = rec.price_unit - percent_amount