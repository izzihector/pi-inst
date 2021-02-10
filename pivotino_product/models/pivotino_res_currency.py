# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Currency(models.Model):
    _inherit = "res.currency"

    position = fields.Selection(default='before')
    active = fields.Boolean(default=False)

    def write(self, values):
        for currency in self:
            if values.get('active') is True:
                pricelist = self.env['product.pricelist'].search(
                    ['|', ('active', '=', True),
                     ('active', '=', False),
                     ('currency_id', '=', currency.id)])
                if pricelist:
                    if pricelist.active is False:
                        pricelist.active = True
                    if pricelist.name != pricelist.currency_id.name:
                        pricelist.name = pricelist.currency_id.name
                else:
                    vals = {
                        'name': currency.name,
                        'currency_id': currency.id
                    }
                    self.env['product.pricelist'].create(vals)
        res = super(Currency, self).write(values)
        return res

    @api.onchange('active')
    def _onchange_active(self):
        if self.active:
            return {
                'warning': {
                    'title': _('Warning!'),
                    'message': _(
                        "The new rate will only be applied for all records that "
                        "are created from this moment. All old records will still be using "
                        "the old rate")}}


class CurrencyRate(models.Model):
    _inherit = "res.currency.rate"

    @api.onchange('name')
    def _onchange_date(self):
        if self.name and self.name < fields.date.today():
            return {
                'warning': {
                    'title': _('Warning!'),
                    'message': _(
                        "The new rate will only be applied for all records that "
                        "are created from this moment. All old records will still be using "
                        "the old rate")}}
