# -*- coding: utf-8 -*-

from odoo import api, fields, models


class MailFeedback(models.TransientModel):
    _name = 'mail.feedback'
    _description = 'Get feedback for mail activity'

    feedback = fields.Text(string='Feedback')

    def action_mail_feedback(self):
        """ Mark the activity as done with the feedback """
        activity = self.env['mail.activity'].browse(
            self.env.context.get('active_ids'))
        return activity.action_feedback(feedback=self.feedback)
