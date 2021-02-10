# -*- coding: utf-8 -*-

import xmlrpc.client
import ssl
from odoo import api, fields, models, _
import logging

_logger = logging.getLogger(__name__)


class Users(models.Model):
    _inherit = 'res.users'

    def submit_positive_feedback_record(self, domain, add_feedback, feedback_tag):
        # get feedback api configuration
        feedback_config = self.env['api.configuration'].search([
            ('is_default', '=', True)
        ], limit=1)

        if feedback_config:
            url = feedback_config.url
            db = feedback_config.db_name
            username = feedback_config.username
            password = feedback_config.password

            # Parameters
            user_name = self.name or ''
            email = self.email or ''
            domain = domain or ''

            try:
                common = xmlrpc.client.ServerProxy(
                    '{}/xmlrpc/2/common'.format(url), verbose=False,
                    context=ssl._create_unverified_context())
                uid = common.authenticate(db, username, password, {})
                models = xmlrpc.client.ServerProxy(
                    '{}/xmlrpc/2/object'.format(url), verbose=False,
                    context=ssl._create_unverified_context())
                models.execute_kw(db, uid, password, 'positive.general.feedback', 'update_positive_feedback',
                                  [uid, user_name, email, domain, add_feedback, feedback_tag])
            except Exception:
                for tag in feedback_tag:
                    code = tag['code']
                    tags = self.env['general.feedback.tags'].search([('code', '=', code)], limit=1)
                    tag_vals = {
                        'username': user_name,
                        'email': email,
                        'domain': domain,
                        'feedback_code': code or '',
                        'feedback_value': tags.value or '',
                        'selected_questions': tag['answer'],
                        'type': 'Positive',
                    }
                    self.env['positive.general.feedback'].create(tag_vals)

                if add_feedback:
                    add_vals = {
                        'username': user_name,
                        'email': email,
                        'domain': domain,
                        'additional_feedback': add_feedback,
                        'type': 'Positive'
                    }
                    self.env['additional.general.feedback'].create(add_vals)

                print('SUBMIT POSITIVE FEEDBACK API CALL FAIL')
                _logger.info('SUBMIT POSITIVE FEEDBACK API CALL FAIL')
                pass
        return True

    def submit_negative_feedback_record(self, domain, add_feedback, feedback_tag):
        # get feedback api configuration
        feedback_config = self.env['api.configuration'].search([
            ('is_default', '=', True)
        ], limit=1)

        if feedback_config:
            url = feedback_config.url
            db = feedback_config.db_name
            username = feedback_config.username
            password = feedback_config.password

            # Parameters
            user_name = self.name or ''
            email = self.email or ''
            domain = domain or ''

            try:
                common = xmlrpc.client.ServerProxy(
                    '{}/xmlrpc/2/common'.format(url), verbose=False,
                    context=ssl._create_unverified_context())
                uid = False
                while not uid:
                    uid = common.authenticate(db, username, password, {})
                models = xmlrpc.client.ServerProxy(
                    '{}/xmlrpc/2/object'.format(url), verbose=False,
                    context=ssl._create_unverified_context())
                models.execute_kw(db, uid, password, 'negative.general.feedback',
                                  'update_negative_feedback',
                                  [uid, user_name, email, domain, add_feedback,
                                   feedback_tag])
            except Exception:
                for tag in feedback_tag:
                    code = tag['code']
                    tags = self.env['general.feedback.tags'].search([('code', '=', code)], limit=1)
                    tag_vals = {
                        'username': user_name,
                        'email': email,
                        'domain': domain,
                        'feedback_code': code or '',
                        'feedback_value': tags.value or '',
                        'selected_questions': tag['answer'],
                        'type': 'Negative',
                    }
                    self.env['negative.general.feedback'].create(tag_vals)

                if add_feedback:
                    add_vals = {
                        'username': user_name,
                        'email': email,
                        'domain': domain,
                        'additional_feedback': add_feedback,
                        'type': 'Negative'
                    }
                    self.env['additional.general.feedback'].create(add_vals)
                    print('WHAT HAPPENNN')

                print('SUBMIT NEGATIVE FEEDBACK API CALL FAIL')
                _logger.info('SUBMIT NEGATIVE FEEDBACK API CALL FAIL')
                pass
        return True
