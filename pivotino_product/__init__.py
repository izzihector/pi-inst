from . import models

from odoo import api, SUPERUSER_ID


def _change_currency_position(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    currency = env['res.currency'].search(['|', ('active', '=', True),
                                           ('active', '=', False)])
    for curr in currency:
        curr.position = 'before'
