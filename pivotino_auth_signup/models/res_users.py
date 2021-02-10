import logging
from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)


class Users(models.Model):
    _inherit = "res.users"

    @classmethod
    def authenticate(cls, db, login, password, user_agent_env):
        """
            Inherit authenticate function
            Refresh the web.base.url config when Business Owner is logged in
        """
        uid = super(Users, cls).authenticate(db, login, password,
                                             user_agent_env)
        if user_agent_env and user_agent_env.get('base_location'):
            with cls.pool.cursor() as cr:
                env = api.Environment(cr, uid, {})
                if env.user.has_group('pivotino_base.group_pivotino_owner'):
                    # Successfully logged in as business owner!
                    # update the web.base.url config
                    try:
                        base = user_agent_env['base_location']
                        icp = env['ir.config_parameter']
                        if not icp.sudo().get_param('web.base.url.freeze'):
                            icp.sudo().set_param('web.base.url', base)
                    except Exception:
                        _logger.exception("Failed to update web.base.url "
                                          "configuration parameter")
        return uid
