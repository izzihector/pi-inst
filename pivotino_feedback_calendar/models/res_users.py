from odoo import models, fields, api, _


class User(models.Model):
    _inherit = 'res.users'

    is_complete_calendar_feedback = fields.Boolean(
        string='Complete calendar creation feedback',
        default=False
    )

    def check_calendar_feedback(self):
        contact_count = self.env['calendar.event'].search_count([
            ('create_uid', '=', self.env.uid)
        ])
        if contact_count >= 2 and not self.is_complete_calendar_feedback:
            return True
        else:
            return False

    def submit_feedback(self, url, feedback, option, is_satisfy):
        if option and option == 'Calendar Creation':
            # use sudo because User do not have the right to write res.users
            self.sudo().write({'is_complete_calendar_feedback': True})
        return super(User, self).submit_feedback(
            url, feedback, option, is_satisfy)
