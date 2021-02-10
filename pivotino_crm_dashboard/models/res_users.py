# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _


class User(models.Model):
    _inherit = 'res.users'

    @api.model
    def change_home_action(self):
        # change the all users' home action after the installing this module
        users = self.env['res.users'].search([])
        users.write({
            'action_id': self.env.ref(
                'pivotino_crm_dashboard.action_pivotino_crm_overview').id
        })

    @api.model
    def create(self, values):
        if not values.get('action_id'):
            values['action_id'] = self.env.ref(
                'pivotino_crm_dashboard.action_pivotino_crm_overview').id
        return super(User, self).create(values)
