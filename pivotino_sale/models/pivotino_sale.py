# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    currency_id = fields.Many2one("res.currency",
                                  string="Currency", readonly=False,
                                  required=True)

    @api.onchange('currency_id')
    def _onchange_currency(self):
        for sale in self:
            pricelist = self.env['product.pricelist'].search(
                [('currency_id', '=', sale.currency_id.id)], limit=1)
            if pricelist:
                partner_pricelist = sale.partner_id.property_product_pricelist
                if partner_pricelist.currency_id == sale.currency_id:
                    sale.pricelist_id = partner_pricelist.id
                else:
                    sale.pricelist_id = pricelist.id
