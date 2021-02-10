from odoo import models, fields, api, _


class PivotinoPasswordWizard(models.TransientModel):
    _name = "pivotino.password.wizard"
    _description = "Pivotino Change Password Wizard"

    new_password = fields.Char(string='New Password', default='')

    def button_change_password(self):
        self.ensure_one()
        # get user from context
        active_id = self._context.get('active_id')
        user = self.env['res.users'].browse(active_id)
        if user:
            # update password
            user.write({'password': self.new_password})
        # don't keep temporary passwords in db
        self.write({'new_password': False})
