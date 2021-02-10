from odoo import models, fields, api, _
import xmlrpc.client
import ssl
import logging

_logger = logging.getLogger(__name__)


class PivotinoFeedback(models.Model):
    _name = 'pivotino.feedback'
    _description = 'Pivotino Feedback Data'

    username = fields.Char(string="Username")
    email = fields.Char(string="Email")
    domain = fields.Char(string="Domain")
    feedback = fields.Text(string="Feedback")
    feedback_tag = fields.Text(string="Feedback Tag")
    is_satisfy = fields.Boolean(string='Satisfied', default=False)
    api_sent = fields.Boolean(string='Sent To Portal', default=False)

    @api.model
    def _cron_api_feedback(self):
        feedback_config = self.env['api.configuration'].search([
            ('is_default', '=', True)
        ], limit=1)
        feedback_lst = []
        feedback_ids = self.search([('api_sent', '=', False)])
        for feedback in feedback_ids:
            feedback_lst.append({
                'username': feedback.username,
                'email': feedback.email,
                'domain': feedback.domain,
                'feedback': feedback.feedback,
                'tag': feedback.feedback_tag,
                'is_satisfy': feedback.is_satisfy,
            })
        try:
            if feedback_config and feedback_lst:
                url = feedback_config.url
                db = feedback_config.db_name
                username = feedback_config.username
                password = feedback_config.password

                common = xmlrpc.client.ServerProxy(
                    '{}/xmlrpc/2/common'.format(url), verbose=False,
                    context=ssl._create_unverified_context())
                uid = common.authenticate(db, username, password, {})
                models = xmlrpc.client.ServerProxy(
                    '{}/xmlrpc/2/object'.format(url), verbose=False,
                    context=ssl._create_unverified_context())
                models.execute_kw(db, uid, password,
                                  'pivotino.feedback',
                                  'cron_update_feedback',
                                  [uid, feedback_lst])
                feedback_ids.write({'api_sent': True})
        except Exception:
            print('CRON ADDITIONAL FEEDBACK API CALL FAIL')
            _logger.info('CRON ADDITIONAL FEEDBACK API CALL FAIL')
