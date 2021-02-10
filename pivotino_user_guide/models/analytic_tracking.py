# -*- coding: utf-8 -*-# -*- coding: utf-8 -*-

from odoo import api, fields, tools, models, _


class AnalyticTracking(models.Model):
    _inherit = 'analytic.tracking'

    @api.model
    def tracking_record_increment_help_button(self):
        """ Add 1 to the analytic tracking record of help button.
        """
        # update analytic tracking help button click count
        help_button_rec = self.env.ref(
            'pivotino_user_guide.analytic_help_button_count')
        record_count = int(help_button_rec.value)
        help_button_rec.value = record_count + 1

    @api.model
    def tracking_record_increment_documentation(self):
        """ Add 1 to the analytic tracking record of documentation link.
        """
        # update analytic tracking documentation link click count
        documentation_button_rec = self.env.ref(
            'pivotino_user_guide.analytic_documentation_count')
        record_count = int(documentation_button_rec.value)
        documentation_button_rec.value = record_count + 1

    @api.model
    def tracking_record_increment_video(self):
        """ Add 1 to the analytic tracking record of video link.
        """
        # update analytic tracking video link click count
        video_button_rec = self.env.ref(
            'pivotino_pre_config.analytic_dashboard_video_count')
        record_count = int(video_button_rec.value)
        video_button_rec.value = record_count + 1
