import xmlrpc.client
import ssl
import logging

_logger = logging.getLogger(__name__)

from odoo import models, fields, api, _


class ResUsers(models.Model):
    _inherit = 'res.users'

    def submit_feedback(self, origin_url, feedback, option, is_satisfy):
        # get feedback api configuration
        feedback_config = self.env['api.configuration'].search([
            ('is_default', '=', True)
        ], limit=1)

        if feedback_config:
            url = feedback_config.url
            db = feedback_config.db_name
            username = feedback_config.username
            password = feedback_config.password
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
                models.execute_kw(db, uid, password, 'pivotino.feedback', 'create',
                                  [{
                                      'username': self.name or '',
                                      'email': self.email or '',
                                      'domain': origin_url or '',
                                      'feedback': feedback or '',
                                      'feedback_tag': option or '',
                                      'is_satisfy': is_satisfy or False,
                                  }])
            except Exception:
                feed_vals = {
                    'username': self.name or '',
                    'email': self.email or '',
                    'domain': origin_url or '',
                    'feedback': feedback or '',
                    'feedback_tag': option or '',
                    'is_satisfy': is_satisfy or False,
                    'api_sent': False,
                }
                self.env['pivotino.feedback'].create(feed_vals)
                print('SUBMIT FEEDBACK API CALL FAIL')
                _logger.info('SUBMIT FEEDBACK API CALL FAIL')
                pass
