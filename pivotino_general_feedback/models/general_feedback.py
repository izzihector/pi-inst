from odoo import api, fields, models, _
import xmlrpc.client
import ssl
import logging

_logger = logging.getLogger(__name__)


class PositiveGeneralFeedback(models.Model):
    _name = "positive.general.feedback"
    _description = "General Feedbacks"

    username = fields.Char(string="Username")
    email = fields.Char(string="Email")
    domain = fields.Char(string="Domain")
    feedback_value = fields.Text(string="Questions")
    feedback_code = fields.Text(string="Feedback Code")
    selected_questions = fields.Char(string='Selected')
    type = fields.Char(string='Type')
    api_sent = fields.Boolean(string='Sent To Portal', default=False)

    @api.model
    def _cron_api_positive_feedback(self):
        feedback_config = self.env['api.configuration'].search([
            ('is_default', '=', True)
        ], limit=1)
        positive_lst = []
        positive_ids = self.search([('api_sent', '=', False)])
        for feedback in positive_ids:
            positive_lst.append({
                'username': feedback.username,
                'email': feedback.email,
                'domain': feedback.domain,
                'code': feedback.feedback_code,
                'value': feedback.feedback_value,
                'selected': feedback.selected_questions,
                'type': feedback.type
            })
        try:
            if feedback_config and positive_lst:
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
                                  'positive.general.feedback',
                                  'cron_update_positive_feedback',
                                  [uid, positive_lst])
                positive_ids.write({'api_sent': True})
        except Exception:
            print('CRON POSITIVE FEEDBACK API CALL FAIL')
            _logger.info('CRON POSITIVE FEEDBACK API CALL FAIL')


class NegativeGeneralFeedback(models.Model):
    _name = "negative.general.feedback"
    _description = "General Feedbacks"

    username = fields.Char(string="Username")
    email = fields.Char(string="Email")
    domain = fields.Char(string="Domain")
    feedback_value = fields.Text(string="Feedback Tag")
    feedback_code = fields.Text(string="Feedback Code")
    selected_questions = fields.Char(string='Selected')
    type = fields.Char(string='Type')
    api_sent = fields.Boolean(string='Sent To Portal', default=False)

    @api.model
    def _cron_api_negative_feedback(self):
        feedback_config = self.env['api.configuration'].search([
            ('is_default', '=', True)
        ], limit=1)
        negative_lst = []
        negative_ids = self.search([('api_sent', '=', False)])
        for feedback in negative_ids:
            negative_lst.append({
                'username': feedback.username,
                'email': feedback.email,
                'domain': feedback.domain,
                'code': feedback.feedback_code,
                'value': feedback.feedback_value,
                'selected': feedback.selected_questions,
                'type': feedback.type
            })
        try:
            if feedback_config and negative_lst:
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
                                  'negative.general.feedback',
                                  'cron_update_negative_feedback',
                                  [uid, negative_lst])
                negative_ids.write({'api_sent': True})
        except Exception:
            print('CRON NEGATIVE FEEDBACK API CALL FAIL')
            _logger.info('CRON NEGATIVE FEEDBACK API CALL FAIL')


class AdditionalGeneralFeedback(models.Model):
    _name = "additional.general.feedback"
    _description = "Additional General Feedbacks"

    username = fields.Char(string="Username")
    email = fields.Char(string="Email")
    domain = fields.Char(string="Domain")
    additional_feedback = fields.Text(string="Additional Feedback")
    type = fields.Char(string="Types")
    api_sent = fields.Boolean(string='Sent To Portal', default=False)

    @api.model
    def _cron_api_additional_feedback(self):
        feedback_config = self.env['api.configuration'].search([
            ('is_default', '=', True)
        ], limit=1)
        additional_lst = []
        additional_ids = self.search([('api_sent', '=', False)])
        for feedback in additional_ids:
            additional_lst.append({
                'username': feedback.username,
                'email': feedback.email,
                'domain': feedback.domain,
                'additional_feedback': feedback.additional_feedback,
                'type': feedback.type,
            })
        try:
            if feedback_config and additional_lst:
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
                                  'additional.general.feedback',
                                  'cron_update_additional_feedback',
                                  [uid, additional_lst])
                additional_ids.write({'api_sent': True})
        except Exception:
            print('CRON ADDITIONAL FEEDBACK API CALL FAIL')
            _logger.info('CRON ADDITIONAL FEEDBACK API CALL FAIL')
