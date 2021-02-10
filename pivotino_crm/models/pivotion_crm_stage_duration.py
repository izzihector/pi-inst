# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class CrmStageDuration(models.Model):
    _name = 'crm.stage.duration'
    _description = 'Duration in CRM Stage'

    lead_id = fields.Many2one('crm.lead', string='Lead', required=1,
                              ondelete='cascade')
    stage_id = fields.Many2one('crm.stage', string='Stage', required=1,
                               ondelete='cascade')
    user_id = fields.Many2one(related='lead_id.user_id',
                              string='Salesperson',
                              store=True)
    company_id = fields.Many2one(related='lead_id.company_id',
                                 string='Company',
                                 store=True)
    stage_start_date = fields.Datetime(string='Stage Start Date')
    stage_end_date = fields.Datetime(string='Stage End Date')
    duration = fields.Float(compute='_compute_stage_duration',
                            string='Stage Duration')

    def _compute_stage_duration(self):
        """ Get the duration between start date and end date
        """
        for rec in self:
            rec.duration = False
            if rec.stage_start_date:
                # if the record has an end date, then find the difference
                # between stage end date and stage start date
                if rec.stage_end_date:
                    duration = rec.stage_end_date - rec.stage_start_date
                    rec.duration = duration.days
                # otherwise, get the today date and find the difference between
                # stage start date and today
                else:
                    now = fields.Datetime.now()
                    duration = now - rec.stage_start_date
                    rec.duration = duration.days
