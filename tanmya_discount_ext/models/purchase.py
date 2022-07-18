from datetime import datetime, time
from itertools import groupby
from odoo import api, fields, models, _
from odoo.tools.float_utils import float_compare, float_is_zero, float_round


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    total_after_discount = fields.Monetary(string='Total After Discount',
                                           compute='_compute_total_after_discount', strore=True)

    total_after_discount_taxes = fields.Monetary(string='Total After Taxes & Discount',
                                                 compute='_compute_total_after_discount', store=True)

    @api.depends('order_line')
    def _compute_total_after_discount(self):
        for rec in self:
            rec.total_after_discount = 0.0
            rec.total_after_discount_taxes = 0.0
            for line in rec.order_line:
                rec.total_after_discount += line.subtotal_after_discount
                rec.total_after_discount_taxes += (line.subtotal_after_discount + line._get_taxes_line_amount())

    def _prepare_invoice(self):
        """Prepare the dict of values to create the new invoice for a purchase order.
        """
        self.ensure_one()
        move_type = self._context.get('default_move_type', 'in_invoice')
        journal = self.env['account.move'].with_context(default_move_type=move_type)._get_default_journal()
        if not journal:
            raise UserError(_('Please define an accounting purchase journal for the company %s (%s).') % (self.company_id.name, self.company_id.id))

        partner_invoice_id = self.partner_id.address_get(['invoice'])['invoice']
        partner_bank_id = self.partner_id.bank_ids.filtered_domain(['|', ('company_id', '=', False), ('company_id', '=', self.company_id.id)])[:1]
        invoice_vals = {
            'ref': self.partner_ref or '',
            'move_type': move_type,
            'narration': self.notes,
            'currency_id': self.currency_id.id,
            'invoice_user_id': self.user_id and self.user_id.id or self.env.user.id,
            'partner_id': partner_invoice_id,
            'fiscal_position_id': (self.fiscal_position_id or self.fiscal_position_id.get_fiscal_position(partner_invoice_id)).id,
            'payment_reference': self.partner_ref or '',
            'partner_bank_id': partner_bank_id.id,
            'invoice_origin': self.name,
            'invoice_payment_term_id': self.payment_term_id.id,
            'invoice_line_ids': [],
            'company_id': self.company_id.id,

            'total_after_discount': self.total_after_discount,
            'total_after_discount_taxes': self.total_after_discount_taxes,
        }
        return invoice_vals


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    discount_percent = fields.Float(string='Disc Percent')
    discount_amount = fields.Float(string='Disc Amount')

    subtotal_after_discount = fields.Monetary(string='Subtotal After Discount',
                                              compute='_compute_subtotal_after_discount', store=True)


    def _get_taxes_line_amount(self):
        total_taxes_amount = 0.0
        for tax in self.taxes_id:
            tax_amount = (tax.amount * self.price_unit) / 100
            total_taxes_amount += tax_amount
        return total_taxes_amount


    @api.depends('discount_percent','discount_amount','price_unit')
    def _compute_subtotal_after_discount(self):
        for rec in self:
            rec.subtotal_after_discount = rec.price_unit
            # rec.subtotal_after_discount = rec.price_unit + rec._get_taxes_line_amount()

            if rec.discount_percent > 0 and rec.discount_amount > 0:
                percent_amount = (rec.price_unit * rec.discount_percent) / 100
                temp_subtotal = rec.price_unit - percent_amount
                rec.subtotal_after_discount = temp_subtotal - rec.discount_amount
                # rec.subtotal_after_discount = rec.subtotal_after_discount + rec._get_taxes_line_amount()

            elif rec.discount_amount > 0:
                rec.subtotal_after_discount = rec.price_unit - rec.discount_amount
                # rec.subtotal_after_discount = rec.subtotal_after_discount + rec._get_taxes_line_amount()

            elif rec.discount_percent > 0:
                percent_amount = (rec.price_unit * rec.discount_percent) / 100
                rec.subtotal_after_discount = rec.price_unit - percent_amount
                # rec.subtotal_after_discount = rec.subtotal_after_discount + rec._get_taxes_line_amount()


    def _prepare_account_move_line(self, move=False):
        self.ensure_one()
        aml_currency = move and move.currency_id or self.currency_id
        date = move and move.date or fields.Date.today()
        res = {
                  'display_type': self.display_type,
                  'sequence': self.sequence,
                  'name': '%s: %s' % (self.order_id.name, self.name),
                  'product_id': self.product_id.id,
                  'product_uom_id': self.product_uom.id,
                  'quantity': self.qty_to_invoice,
                  'price_unit': self.currency_id._convert(self.price_unit, aml_currency, self.company_id, date,
                                                          round=False),
                  'tax_ids': [(6, 0, self.taxes_id.ids)],
                  'analytic_account_id': self.account_analytic_id.id,
                  'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
                  'purchase_line_id': self.id,

                  'discount_percent': self.discount_percent,
                  'discount_amount': self.discount_amount,
                  'subtotal_after_discount': self.subtotal_after_discount,
        }
        if not move:
            return res

        if self.currency_id == move.company_id.currency_id:
            currency = False
        else:
            currency = move.currency_id

        res.update({
            'move_id': move.id,
            'currency_id': currency and currency.id or False,
            'date_maturity': move.invoice_date_due,
            'partner_id': move.partner_id.id,
        })
        return res




