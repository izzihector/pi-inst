# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    type = fields.Selection([
        ('consu', 'Consumable'),
        ('service', 'Service')], string='Product Type', default='service',
        required=True,
        readonly=True,
        help='A storable product is a product for which you manage stock. The Inventory app has to be installed.\n'
             'A consumable product is a product for which stock is not managed.\n'
             'A service is a non-material product you provide.')
    purchase_ok = fields.Boolean('Can be Purchased', default=False)
