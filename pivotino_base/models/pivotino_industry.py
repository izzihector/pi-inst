# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class PivotinoIndustry(models.Model):
    _name = "pivotino.industry"
    _description = "Pivotino Industry"

    name = fields.Char(string='Industry Name')
    is_others = fields.Boolean(string='Others?', default=False)
