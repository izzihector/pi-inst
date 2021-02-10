# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Pricelist(models.Model):
    _inherit = 'product.pricelist'

    def _get_partner_pricelist_multi_search_domain_hook(self, company_id):
        """ inherit this function to return the correct pricelist based on
        company currency """
        res = super(Pricelist, self).\
            _get_partner_pricelist_multi_search_domain_hook(company_id)
        res.append(
            ('currency_id', '=', self.env.company.currency_id.id)
        )
        return res
