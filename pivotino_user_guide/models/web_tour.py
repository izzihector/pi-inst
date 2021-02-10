# -*- coding: utf-8 -*-# -*- coding: utf-8 -*-

from odoo import api, fields, tools, models, _


class Tour(models.Model):
    _inherit = 'web_tour.tour'

    @api.model
    def consume(self, tour_names):
        """ Increment the analytic tracking record """
        res = super(Tour, self).consume(tour_names)
        for rec in tour_names:
            # update analytic tracking tour count
            tour_count_rec = self.env.ref(
                'pivotino_user_guide.analytic_tour_count')
            tour_count_rec.tracking_record_increment_integer(1)
        return res
