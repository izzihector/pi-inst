# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class Import(models.TransientModel):
    _inherit = 'base_import.import'

    def do(self, fields, columns, options, dryrun=False):
        # update analytic tracking import count
        import_count_rec = self.env.ref(
            'pivotino_base_import.analytic_import_count')
        import_count_rec.tracking_record_increment_integer(1)

        return super(Import, self).do(fields, columns, options, dryrun)
