import logging
import xmlrpc.client
import ssl

from odoo import api, SUPERUSER_ID

_logger = logging.getLogger(__name__)


def _check_instance_status(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    config = env['api.configuration'].search([('is_default', '=', True)])
    current_db = env.cr.dbname
    url = config.url
    db = config.db_name
    username = config.username
    password = config.password
    common = xmlrpc.client.ServerProxy(
        '{}/xmlrpc/2/common'.format(url), verbose=False,
        context=ssl._create_unverified_context())
    uid = common.authenticate(db, username, password, {})
    models = xmlrpc.client.ServerProxy(
        '{}/xmlrpc/2/object'.format(url), verbose=False,
        context=ssl._create_unverified_context())
    models.execute_kw(db, uid, password, 'res.users', 'check_status_bool',
                      [current_db])

