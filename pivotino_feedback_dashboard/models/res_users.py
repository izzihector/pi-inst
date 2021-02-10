from odoo import models, fields, api, _


class Users(models.Model):
    _inherit = 'res.users'

    is_complete_missed_sale_feedback = fields.Boolean(
        string='Complete Missed Sale Feedback',
        default=False
    )
    is_complete_sale_target_feedback = fields.Boolean(
        string='Complete Sale vs Target Feedback',
        default=False
    )

    def check_dashboard_feedback(self):
        # initialise a dict for verification
        dashboard_feedback = {
            'lost': False,
            'won': False
        }
        # get lost opportunity count
        lost_count = self.env['crm.lead'].search_count([
            ('is_lost', '=', True),
            ('type', '=', 'opportunity'),
            ('user_id', '=', self.env.uid)
        ])
        # get won opportunity count
        won_count = self.env['crm.lead'].search_count([
            ('is_won', '=', True),
            ('type', '=', 'opportunity'),
            ('user_id', '=', self.env.uid)
        ])
        # check lost count condition
        if lost_count >= 3 and not self.is_complete_missed_sale_feedback:
            dashboard_feedback['lost'] = True
        else:
            dashboard_feedback['lost'] = False
        # check won count condition
        if won_count >= 3 and not self.is_complete_sale_target_feedback:
            dashboard_feedback['won'] = True
        else:
            dashboard_feedback['won'] = False
        return dashboard_feedback

    def submit_feedback(self, url, feedback, option, is_satisfy):
        if option and option == 'Missed Sales':
            # use sudo because User do not have the right to write res.users
            self.sudo().write({'is_complete_missed_sale_feedback': True})
        if option and option == 'Actual Sales':
            # use sudo because User do not have the right to write res.users
            self.sudo().write({'is_complete_sale_target_feedback': True})
        return super(Users, self).submit_feedback(
            url, feedback, option, is_satisfy)
