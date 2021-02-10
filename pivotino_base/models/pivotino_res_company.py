# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError


class Company(models.Model):
    _inherit = 'res.company'

    industry = fields.Many2one('pivotino.industry', string='Industry')
    currency_id = fields.Many2one('res.currency',
                                  string='Base Currency',
                                  required=True,
                                  default=lambda self: self._get_user_currency())

    @api.constrains('currency_id')
    def _base_currency_rate(self):
        for company in self:
            if company.currency_id.rate != 1:
                raise ValidationError(_('The currency rate for base currency '
                                        'should be 1. \n'
                                        'You may change the rate under '
                                        'Sales > Currencies '))
