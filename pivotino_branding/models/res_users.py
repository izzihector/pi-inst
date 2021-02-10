from odoo import models, fields, api, _


class Users(models.Model):
    _inherit = 'res.users'

    odoobot_state = fields.Selection(string='PivotinoBot Status')

    def preference_change_password(self):
        res = super(Users, self).preference_change_password()
        # add name to the wizard, default is "Odoo"
        res.update({
            'name': _('Pivotino'),
        })
        return res
