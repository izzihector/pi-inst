# -*- coding: utf-8 -*-

from odoo import api, fields, models
from dateutil.relativedelta import relativedelta


class MailActivity(models.Model):
    _inherit = 'mail.activity'
    _description = 'Activity'

    def _action_done(self, feedback=False, attachment_ids=None):
        activity_type = self.env.ref('pivotino_crm.mail_activity_first_activity')
        if self.res_id and self.activity_type_id == activity_type:
            if not self.env.context.get('from_lead'):
                lead_id = self.env['crm.lead'].search([('id', '=', self.res_id)])
                lead_id.with_context(action_done=True).write({
                    'stage_id': self.env.ref('crm.stage_lead2').id
                })
                if len(lead_id.activity_ids) <= 1:
                    for act in lead_id.activity_ids:
                        if act.id == self.id:
                            activity_vals = self._get_todo_activity_values(lead_id)
                            self.create(activity_vals)
        res = super(MailActivity, self)._action_done(feedback, attachment_ids)
        return res

    @api.model
    def create(self, vals):
        res = super(MailActivity, self).create(vals)
        days_lost = self.env.user.company_id.day_set_lost
        if res.res_model_id.model == 'crm.lead':
            lead = self.env['crm.lead'].search([('id', '=', res.res_id)])
            if lead:
                act = self.search([('res_id', '=', lead.id)])
                latest_date_act = act[0]
                for all in act:
                    if all.date_deadline > latest_date_act.date_deadline:
                        latest_date_act = all
                if not lead.date_manual_deadline:
                    if res.date_deadline >= latest_date_act.date_deadline:
                        days = res.date_deadline + relativedelta(days=days_lost)
                        lead.with_context(from_activity=True).write({
                            'date_deadline': days,
                        })
        return res

    def write(self, values):
        res = super(MailActivity, self).write(values)
        days_lost = self.env.user.company_id.day_set_lost
        for mail in self:
            if mail.res_model_id.model == 'crm.lead':
                lead = self.env['crm.lead'].search([('id', '=', mail.res_id)])
                if lead:
                    act = self.search([('res_id', '=', lead.id)])
                    latest_date_act = act[0]
                    for all in act:
                        if all.date_deadline > latest_date_act.date_deadline:
                            latest_date_act = all
                    if not lead.date_manual_deadline:
                        if mail.date_deadline >= latest_date_act.date_deadline:
                            days = mail.date_deadline + relativedelta(days=days_lost)
                            lead.with_context(from_activity=True).write({
                                'date_deadline': days,
                            })
        return res

    def _get_todo_activity_values(self, lead_id):
        activity_type = self.env.ref('mail.mail_activity_data_todo')
        base = fields.Date.context_today(self)
        date_deadline = base + relativedelta(
            **{activity_type.delay_unit: activity_type.delay_count})
        summary = 'Follow Up'
        user = activity_type.default_user_id or self.env.user
        note = 'System has helped you to schedule this activity. ' \
               'Please continue to follow up on this opportunity.'
        res_model = self.env['ir.model']._get('crm.lead').id

        return {
            'summary': summary,
            'activity_type_id': activity_type.id,
            'res_model_id': res_model,
            'res_id': lead_id,
            'date_deadline': date_deadline,
            'user_id': user.id,
            'note': note
        }


class MailActivityType(models.Model):
    _inherit = 'mail.activity.type'
    _description = 'Activity Type'
