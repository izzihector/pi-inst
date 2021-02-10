# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class MailActivity(models.Model):
    _inherit = 'mail.activity'

    def action_view_document(self):
        """ View the source document of the mail activity
        """
        self.ensure_one()
        return {
            'name': _(self.res_name),
            'res_model': self.res_model,
            'view_mode': 'tree,form',
            'view_type': 'form',
            'views': [(False, 'form')],
            'type': 'ir.actions.act_window',
            'res_id': self.res_id,
        }

    def _action_done(self, feedback=False, attachment_ids=None):
        res = super(MailActivity, self)._action_done(feedback, attachment_ids)
        for rec in self:
            # update analytic tracking mail activity count
            activity_count_rec = self.env.ref(
                'pivotino_mail.analytic_activity_count')
            activity_count_rec.tracking_record_increment_integer(1)
        return res
