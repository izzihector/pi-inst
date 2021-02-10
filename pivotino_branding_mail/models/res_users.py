# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class Users(models.Model):
    _inherit = 'res.users'

    notification_type = fields.Selection([
        ('email', 'Handle by Emails'),
        ('inbox', 'Handle in Pivotino')],
        help="Policy on how to handle Chatter notifications:\n"
             "- Handle by Emails: notifications are sent to your email "
             "address\n"
             "- Handle in Pivotino: notifications appear in your Pivotino "
             "Inbox"
    )
