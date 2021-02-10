# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError


class CurrencyRate(models.Model):
    _inherit = 'res.currency.rate'

    @api.constrains('rate')
    def _check_base_currency_rate(self):
        for curr in self:
            if curr.company_id == self.env.company \
                    and curr.currency_id == curr.company_id.currency_id \
                    and curr.rate != 1:
                raise ValidationError(_('The currency %s is a base currency and'
                                        ' should have rate of 1.')
                                      % curr.currency_id.name)
