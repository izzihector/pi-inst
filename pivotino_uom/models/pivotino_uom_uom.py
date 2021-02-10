# -*- coding: utf-8 -*-

from odoo import api, fields, tools, models, _


class UoM(models.Model):
    _inherit = 'uom.uom'

    category_id = fields.Many2one(
        'uom.category', 'Category', required=True, ondelete='cascade',
        help="Conversion between Units of Measure can only occur if "
             "they belong to the same category. The conversion will be "
             "made based on the ratios.", default=lambda self: self.env['uom.category'].search([('id', '=', self.env.ref('uom.product_uom_categ_unit').id)]))
    uom_type = fields.Selection([
        ('bigger', 'Bigger than the reference Unit of Measure'),
        ('reference', 'Reference Unit of Measure for this category'),
        ('smaller', 'Smaller than the reference Unit of Measure')], 'Type',
        default='bigger', required=1)


class UoMCategory(models.Model):
    _inherit = 'uom.category'

    measure_type = fields.Selection([
        ('unit', 'Default Units'),
        ('weight', 'Default Weight'),
        ('working_time', 'Default Working Time'),
        ('length', 'Default Length'),
        ('volume', 'Default Volume'),
        ('default_1', 'Default Measurement 1'),
        ('default_2', 'Default Measurement 2'),
        ('default_3', 'Default Measurement 3'),
        ('default_4', 'Default Measurement 4'),
        ('default_5', 'Default Measurement 5'),
    ], string="Type of Measure")
