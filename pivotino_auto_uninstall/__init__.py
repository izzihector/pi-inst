import logging

from odoo import api, SUPERUSER_ID

_logger = logging.getLogger(__name__)


def _uninstall_modules(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    # uninstall iap
    iap_module = env['ir.module.module'].search([
        ('name', '=', 'iap')
    ])
    iap_module.button_uninstall()
    # uninstall odoo_referral
    referral_module = env['ir.module.module'].search([
        ('name', '=', 'odoo_referral')
    ])
    referral_module.button_uninstall()
