# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import api, fields, models, tools, SUPERUSER_ID, _

from odoo.http import request
from odoo.addons.website.models import ir_http
from odoo.addons.http_routing.models.ir_http import url_for

_logger = logging.getLogger(__name__)


class BookingWebsite(models.Model):
    _inherit = 'website'
    
    def sale_get_order(self, force_create=False, code=None, update_pricelist=False, force_pricelist=False):

        # ensure last sale order is not last booking order
        self.ensure_one()
        partner = self.env.user.partner_id
        sale_order_id = request.session.get('sale_order_id')
        if not sale_order_id and not self.env.user._is_public():
            last_order = partner.last_website_so_id
            if last_order.booking_order:
                partner.last_website_so_id = None
        return super(BookingWebsite, self).sale_get_order(force_create, code, update_pricelist, force_pricelist)

    def booking_get_order(self, force_create=False, code=None, update_pricelist=False, force_pricelist=False):
        """ Return the current sales order after mofications specified by params.
        :param bool force_create: Create sales order if not already existing
        :param str code: Code to force a pricelist (promo code)
                         If empty, it's a special case to reset the pricelist with the first available else the default.
        :param bool update_pricelist: Force to recompute all the lines from sales order to adapt the price with the current pricelist.
        :param int force_pricelist: pricelist_id - if set,  we change the pricelist with this one
        :returns: browse record for the current sales order
        """

        self.ensure_one()
        partner = self.env.user.partner_id
        booking_order_id = request.session.get('booking_order_id')
        check_fpos = False
        # Test validity of the booking_order_id
        sale_order = self.env['sale.order'].with_company(request.website.company_id.id).sudo().browse(booking_order_id).exists() if booking_order_id else None

        # Do not reload the cart of this user last visit if the Fiscal Position has changed.
        if check_fpos and sale_order:
            fpos_id = (
                self.env['account.fiscal.position'].sudo()
                .with_company(sale_order.company_id.id)
                .get_fiscal_position(sale_order.partner_id.id, delivery_id=sale_order.partner_shipping_id.id)
            ).id
            if sale_order.fiscal_position_id.id != fpos_id:
                sale_order = None

        if not (sale_order or force_create or code):
            print("order is null and order_session_id is:", request.session.get('booking_order_id'))
            if request.session.get('booking_order_id'):
                request.session['booking_order_id'] = None

            return self.env['sale.order']

        if self.env['product.pricelist'].browse(force_pricelist).exists():
            pricelist_id = force_pricelist
            request.session['website_sale_current_pl'] = pricelist_id
            update_pricelist = True
        else:
            pricelist_id = request.session.get('website_sale_current_pl') or self.get_current_pricelist().id

        if not self._context.get('pricelist'):
            self = self.with_context(pricelist=pricelist_id)

        # cart creation was requested (either explicitly or to configure a promo code)
        if not sale_order:
            # TODO cache partner_id session
            pricelist = self.env['product.pricelist'].browse(pricelist_id).sudo()
            so_data = self._prepare_sale_order_values(partner, pricelist)
            so_data['booking_order'] = True
            sale_order = self.env['sale.order'].with_company(request.website.company_id.id).with_user(SUPERUSER_ID).create(so_data)

            # set fiscal position
            if request.website.partner_id.id != partner.id:
                sale_order.onchange_partner_shipping_id()
            else: # For public user, fiscal position based on geolocation
                country_code = request.session['geoip'].get('country_code')
                if country_code:
                    country_id = request.env['res.country'].search([('code', '=', country_code)], limit=1).id
                    sale_order.fiscal_position_id = request.env['account.fiscal.position'].sudo().with_company(request.website.company_id.id)._get_fpos_by_region(country_id)
                else:
                    # if no geolocation, use the public user fp
                    sale_order.onchange_partner_shipping_id()

            request.session['booking_order_id'] = sale_order.id

        # case when user emptied the cart
        if not request.session.get('booking_order_id'):
            request.session['booking_order_id'] = sale_order.id

        # check for change of pricelist with a coupon
        pricelist_id = pricelist_id or partner.property_product_pricelist.id

        # check for change of partner_id ie after signup
        if sale_order.partner_id.id != partner.id and request.website.partner_id.id != partner.id:
            flag_pricelist = False
            if pricelist_id != sale_order.pricelist_id.id:
                flag_pricelist = True
            fiscal_position = sale_order.fiscal_position_id.id

            # change the partner, and trigger the onchange
            sale_order.write({'partner_id': partner.id})
            sale_order.with_context(not_self_saleperson=True).onchange_partner_id()
            sale_order.write({'partner_invoice_id': partner.id})
            sale_order.onchange_partner_shipping_id() # fiscal position
            sale_order['payment_term_id'] = self.sale_get_payment_term(partner)

            # check the pricelist : update it if the pricelist is not the 'forced' one
            values = {}
            if sale_order.pricelist_id:
                if sale_order.pricelist_id.id != pricelist_id:
                    values['pricelist_id'] = pricelist_id
                    update_pricelist = True

            # if fiscal position, update the order lines taxes
            if sale_order.fiscal_position_id:
                sale_order._compute_tax_id()

            # if values, then make the SO update
            if values:
                sale_order.write(values)

            # check if the fiscal position has changed with the partner_id update
            recent_fiscal_position = sale_order.fiscal_position_id.id
            # when buying a free product with public user and trying to log in, SO state is not draft
            if (flag_pricelist or recent_fiscal_position != fiscal_position) and sale_order.state == 'draft':
                update_pricelist = True

        if code and code != sale_order.pricelist_id.code:
            code_pricelist = self.env['product.pricelist'].sudo().search([('code', '=', code)], limit=1)
            if code_pricelist:
                pricelist_id = code_pricelist.id
                update_pricelist = True
        elif code is not None and sale_order.pricelist_id.code and code != sale_order.pricelist_id.code:
            # code is not None when user removes code and click on "Apply"
            pricelist_id = partner.property_product_pricelist.id
            update_pricelist = True

        # update the pricelist
        if update_pricelist:
            request.session['website_sale_current_pl'] = pricelist_id
            values = {'pricelist_id': pricelist_id}
            sale_order.write(values)
            for line in sale_order.order_line:
                if line.exists():
                    sale_order._cart_update(product_id=line.product_id.id, line_id=line.id, add_qty=0)
        print("booking order",sale_order)
        return sale_order

    def get_current_pricelist(self):
        """
        :returns: The current pricelist record
        """
        # The list of available pricelists for this user.
        # If the user is signed in, and has a pricelist set different than the public user pricelist
        # then this pricelist will always be considered as available
        available_pricelists = self.get_pricelist_available()
        pl = None
        partner = self.env.user.partner_id
        if request and request.session.get('website_sale_current_pl'):
            # `website_sale_current_pl` is set only if the user specifically chose it:
            #  - Either, he chose it from the pricelist selection
            #  - Either, he entered a coupon code
            pl = self.env['product.pricelist'].browse(request.session['website_sale_current_pl'])
            if pl not in available_pricelists:
                pl = None
                request.session.pop('website_sale_current_pl')
        if not pl:
            current_url = request.httprequest.url_root[:-1] + (
                    hasattr(request, 'rerouting') and request.rerouting[0] or request.httprequest.path)

            # If the user has a saved cart, it take the pricelist of this last unconfirmed cart
            pl = partner.last_website_booking_id.pricelist_id if 'booking' in current_url else partner.last_website_so_id.pricelist_id
            if not pl:
                # The pricelist of the user set on its partner form.
                # If the user is not signed in, it's the public user pricelist
                pl = partner.property_product_pricelist
            if available_pricelists and pl not in available_pricelists:
                # If there is at least one pricelist in the available pricelists
                # and the chosen pricelist is not within them
                # it then choose the first available pricelist.
                # This can only happen when the pricelist is the public user pricelist and this pricelist is not in the available pricelist for this localization
                # If the user is signed in, and has a special pricelist (different than the public user pricelist),
                # then this special pricelist is amongs these available pricelists, and therefore it won't fall in this case.
                pl = available_pricelists[0]

        if not pl:
            _logger.error('Fail to find pricelist for partner "%s" (id %s)', partner.name, partner.id)
        return pl

    def _get_pricelist_available(self, req, show_visible=False):
        """ Return the list of pricelists that can be used on website for the current user.
        Country restrictions will be detected with GeoIP (if installed).
        :param bool show_visible: if True, we don't display pricelist where selectable is False (Eg: Code promo)
        :returns: pricelist recordset
        """
        website = ir_http.get_request_website()
        if not website:
            if self.env.context.get('website_id'):
                website = self.browse(self.env.context['website_id'])
            else:
                # In the weird case we are coming from the backend (https://github.com/odoo/odoo/issues/20245)
                website = len(self) == 1 and self or self.search([], limit=1)
        isocountry = req and req.session.geoip and req.session.geoip.get('country_code') or False
        partner = self.env.user.partner_id
        current_url = request.httprequest.url_root[:-1] + (
                hasattr(request, 'rerouting') and request.rerouting[0] or request.httprequest.path)
        last_order_pl = partner.last_website_booking_id.pricelist_id if 'booking' in current_url else partner.last_website_so_id.pricelist_id
        partner_pl = partner.property_product_pricelist
        pricelists = website._get_pl_partner_order(isocountry, show_visible,
                                                   website.user_id.sudo().partner_id.property_product_pricelist.id,
                                                   req and req.session.get('website_sale_current_pl') or None,
                                                   website.pricelist_ids,
                                                   partner_pl=partner_pl and partner_pl.id or None,
                                                   order_pl=last_order_pl and last_order_pl.id or None)
        return self.env['product.pricelist'].browse(pricelists)

    def sale_reset(self):
        request.session.update({
            'sale_order_id': False,
            'booking_order_id': False,
            'website_sale_current_pl': False,
        })