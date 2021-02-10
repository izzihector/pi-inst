from odoo import models, fields, api, _


class User(models.Model):
    _inherit = 'res.users'

    is_complete_crm_feedback = fields.Boolean(
        string='Complete lead creation feedback',
        default=False
    )

    def check_crm_feedback(self):
        opportunity_count = self.env['crm.lead'].search_count([
            ('create_uid', '=', self.env.uid),
            ('type', '=', 'opportunity'),
        ])
        if opportunity_count >= 2 and not self.is_complete_crm_feedback:
            return True
        else:
            return False

    def submit_feedback(self, url, feedback, option, is_satisfy):
        if option and option == 'Opportunity Creation':
            # use sudo because User do not have the right to write res.users
            self.sudo().write({'is_complete_crm_feedback': True})
        return super(User, self).submit_feedback(
            url, feedback, option, is_satisfy)
