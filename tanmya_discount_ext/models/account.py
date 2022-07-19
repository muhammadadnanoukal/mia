from odoo import api, fields, models



class AccountMove(models.Model):
    _inherit = "account.move"



    total_discount = fields.Monetary(string='Total Discount', compute='_compute_total_discount', store=True)
    total_taxes_after_discount = fields.Monetary(string='Taxes After Discount',
                                                 compute='_compute_total_taxes_after_discount', store=True)
    total_after_discount = fields.Monetary(string='Total After Discount',
                                           compute='_compute_total_after_discount', store=True)


    @api.depends('line_ids')
    def _compute_total_discount(self):
        for rec in self:
            rec.total_discount = 0.0
            for line in rec.line_ids:
                if line.product_id:
                    rec.total_discount += line.get_discount_line_amount()

    @api.depends('line_ids')
    def _compute_total_taxes_after_discount(self):
        for rec in self:
            rec.total_taxes_after_discount = 0.0
            for line in rec.line_ids:
                if line.product_id:
                    rec.total_taxes_after_discount += line.get_taxes_line_amount()

    @api.depends('line_ids')
    def _compute_total_after_discount(self):
        for rec in self:
            rec.total_after_discount = 0.0
            for line in rec.line_ids:
                if line.product_id:
                    rec.total_after_discount += (line.subtotal_after_discount + line.get_taxes_line_amount())


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    discount_percent = fields.Float(string='Disc Percent')
    discount_amount = fields.Float(string='Disc Amount')
    subtotal_after_discount = fields.Monetary(string='Subtotal After Discount',
                                              compute='_compute_subtotal_after_discount', store=True)


    def get_taxes_line_amount(self):
        total_taxes_amount = 0.0

        for tax in self.tax_ids:
            tax_amount = (tax.amount * self.subtotal_after_discount) / 100
            total_taxes_amount += tax_amount

        if total_taxes_amount == 0:
            for tax in self.tax_ids:
                total_taxes_amount += ((tax.amount * self.price_unit) / 100)

        return total_taxes_amount

    def get_discount_line_amount(self):
        line_discount = 0.0
        if self.discount_percent > 0 and self.discount_amount > 0:
            percent_value = (self.price_unit * self.discount_percent) / 100
            amount_value = self.discount_amount
            line_discount = percent_value + amount_value

        elif self.discount_amount > 0:
            amount_value = self.discount_amount
            line_discount = amount_value

        elif self.discount_percent > 0:
            percent_value = (self.price_unit * self.discount_percent) / 100
            line_discount = percent_value

        return line_discount

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