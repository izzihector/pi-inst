# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Users(models.Model):
    _inherit = 'res.users'

    @api.model
    def get_activity_summary_count(self, user_id):
        """ Get the activity summary count """
        user = self.browse(user_id)
        if user.has_group('pivotino_base.group_pivotino_owner'):
            activity = self.env['mail.activity'].search([])
        else:
            activity = self.env['mail.activity'].search([
                ('user_id', '=', user_id)])
        future_due_activity = activity.filtered(lambda m: m.state == 'planned')
        today_activity = activity.filtered(lambda m: m.state == 'today')
        overdue_activity = activity.filtered(lambda m: m.state == 'overdue')

        future_due_activity_count = len(future_due_activity) or 0
        today_activity_count = len(today_activity) or 0
        overdue_activity_count = len(overdue_activity) or 0
        all_activity_count = len(activity) or 0
        res = {
            'all_activity_count': all_activity_count,
            'future_due_activity_count': future_due_activity_count,
            'today_activity_count': today_activity_count,
            'overdue_activity_count': overdue_activity_count
        }
        return res

    @api.model
    def get_activity_summary(self, user_id):
        """ Get the activity summary view """
        return self.env['ir.ui.view'].with_context().render_template(
            'pivotino_mail.pivotino_activity_count_box',
            self.get_activity_summary_count(user_id)
        )

    @api.model
    def get_all_activity(self, user_id):
        """ Get the all mail_activity ids that the user is allowed to read"""
        user = self.browse(user_id)
        if user.has_group('pivotino_base.group_pivotino_owner'):
            activity = self.env['mail.activity'].search([])
        else:
            activity = self.env['mail.activity'].search([
                ('user_id', '=', user_id)])
        res = activity.ids
        return res

    @api.model
    def get_future_due_activity(self, user_id):
        """ Get the future due mail_activity ids that the user is allowed to
        read"""
        user = self.browse(user_id)
        if user.has_group('pivotino_base.group_pivotino_owner'):
            activity = self.env['mail.activity'].search([])
        else:
            activity = self.env['mail.activity'].search([
                ('user_id', '=', user_id)])
        future_due_activity = activity.filtered(
            lambda m: m.state == 'planned')
        res = future_due_activity.ids
        return res

    @api.model
    def get_today_activity(self, user_id):
        """ Get the today mail_activity ids that the user is allowed to read"""
        user = self.browse(user_id)
        if user.has_group('pivotino_base.group_pivotino_owner'):
            activity = self.env['mail.activity'].search([])
        else:
            activity = self.env['mail.activity'].search([
                ('user_id', '=', user_id)])
        today_activity = activity.filtered(
            lambda m: m.state == 'today')
        res = today_activity.ids
        return res

    @api.model
    def get_overdue_activity(self, user_id):
        """ Get the overdue mail_activity ids that the user is allowed to
        read"""
        user = self.browse(user_id)
        if user.has_group('pivotino_base.group_pivotino_owner'):
            activity = self.env['mail.activity'].search([])
        else:
            activity = self.env['mail.activity'].search([
                ('user_id', '=', user_id)])
        overdue_activity = activity.filtered(
            lambda m: m.state == 'overdue')
        res = overdue_activity.ids
        return res
