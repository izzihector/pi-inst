import operator

from odoo import models, fields, api, _, tools, modules


class Users(models.Model):
    _inherit = 'res.users'

    @api.model
    def systray_get_activities(self):
        res = super(Users, self).systray_get_activities()
        # temporarily use this way to change the activity icon..
        # as not yet got all the new icons for all apps
        for activity in res:
            # calendar activity
            if activity['model'] == 'calendar.event':
                activity['icon'] = modules.module.get_module_icon(
                    'pivotino_branding_calendar')
            # crm activity
            if activity['model'] == 'crm.lead':
                activity['icon'] = modules.module.get_module_icon(
                    'pivotino_branding_crm')
            # contact activity
            if activity['model'] == 'res.partner':
                activity['icon'] = modules.module.get_module_icon(
                    'pivotino_branding_contacts')
        return res
