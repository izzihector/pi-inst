# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _


class Company(models.Model):
    _inherit = 'res.company'

    # To do: Update the field type (ZEN)
    day_set_lost = fields.Integer(string='Day(s) to set to LOST', default=7)
    day_set_due = fields.Integer(string='Day(s) to set DUE for each activity',
                                 default=7)
    default_sale_target = fields.Float(string='Sales Target for Company')
    auto_lead = fields.Boolean(string='Auto Create Lead From SO',
                               default=True)

    @api.onchange('day_set_due')
    def change_activity_date(self):
        # write the day_set_due to all activity type
        activity_types = self.env['mail.activity.type'].search([])
        for activity_type in activity_types:
            activity_type.write({
                'delay_count': self.day_set_due
            })


class User(models.Model):
    _inherit = 'res.users'

    sale_ids = fields.One2many('sale.order', 'user_id', string='Sale')

    @api.model
    def systray_get_activities(self):
        res = super(User, self).systray_get_activities()
        # rename 'Lead/Opportunity' to 'Opportunity' for crm systray activity
        for activity in res:
            if activity['model'] == 'crm.lead':
                activity['name'] = 'Opportunity'
        return res
