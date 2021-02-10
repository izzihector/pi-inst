# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import xmlrpc.client
import ssl
import logging

_logger = logging.getLogger(__name__)


class Users(models.Model):
    _inherit = 'res.users'

    login_date_1 = fields.Datetime(related='log_ids.create_date', string='Latest authentication', readonly=False, store=True)
    first_log_bool = fields.Boolean(string='Test', default=False)
    clogin = fields.Boolean(default=False)
    starter_view_id = fields.Integer(string='Starter Kit ID', copy=False)

    @api.model
    def _update_last_login(self):
        all_user = self.search([('login_date_1', '!=', False)])
        if all_user:
            for user in self.search([]):
                user.sudo().write({
                    'first_log_bool': True,
                })

        # Call Portal API and write into res.users when user first logged in
        first_login_track_user = self.env['ir.config_parameter']
        api_config = self.env['api.configuration'].search([
            ('is_default', '=', True)
        ], limit=1)
        url = api_config.url
        db = api_config.db_name
        username = api_config.username
        password = api_config.password
        common = xmlrpc.client.ServerProxy(
            '{}/xmlrpc/2/common'.format(url),
            verbose=False,
            context=ssl._create_unverified_context())
        # get the unique db name as domain
        dbname = self.env.cr.dbname
        # update only the latest authentication date of the instance owner
        if self.customer_client_id and self.customer_client_id != 0:
            try:
                uid = common.authenticate(db, username, password, {})
                models = xmlrpc.client.ServerProxy(
                    '{}/xmlrpc/2/object'.format(url), verbose=False,
                    context=ssl._create_unverified_context())
                models.execute_kw(db, uid, password, 'res.users',
                                  'update_instance_login', [dbname])
            except Exception:
                print('UPDATE LAST LOGIN API CALL FAIL')
                _logger.info('UPDATE LAST LOGIN API CALL FAIL')
                pass

        return super(Users, self)._update_last_login()

    @api.onchange('user_role')
    def _check_user_type(self):
        if self.user_role == 'owner':
            self.starter_view_id = self.env.ref('pivotino_pre_config.starter_wizard_view_video_bo').id
        else:
            self.starter_view_id = self.env.ref('pivotino_pre_config.starter_wizard_view_video').id
