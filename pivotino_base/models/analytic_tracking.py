# -*- coding: utf-8 -*-

from odoo import api, fields, tools, models, _


class AnalyticTracking(models.Model):
    _name = 'analytic.tracking'
    _description = 'Analytic Tracking'

    name = fields.Char('Name', required=True)
    value = fields.Char('Value', required=True)

    def tracking_record_increment_integer(self, value):
        """ Add 1 to the analytic tracking record.
        This function is useful for integer value record.
        """
        for rec in self:
            record_count = int(rec.value)
            rec.value = record_count + value
