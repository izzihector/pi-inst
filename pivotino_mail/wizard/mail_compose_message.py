# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class MailComposer(models.TransientModel):
    _inherit = 'mail.compose.message'

    def action_send_mail(self):
        # update analytic tracking mail count
        mail_count_rec = self.env.ref('pivotino_mail.analytic_mail_count')
        mail_count_rec.tracking_record_increment_integer(1)

        return super(MailComposer, self).action_send_mail()
