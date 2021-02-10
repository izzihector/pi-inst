# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def get_import_templates(self):
        return [{
            'label': _('Import Template for Products'),
            'template': '/pivotino_sale/static/xls/product_template.xls'
        }]
