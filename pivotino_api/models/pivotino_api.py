from odoo import models, fields, api, _
from odoo.exceptions import UserError


class APIConfiguration(models.Model):
    _name = 'api.configuration'
    _description = 'Pivotino API Configuration'

    url = fields.Char(string='URL')
    db_name = fields.Char(string='Database')
    username = fields.Char(string='Username')
    password = fields.Char(string='Password')
    is_default = fields.Boolean(string='Default', default=False)

    @api.constrains('is_default')
    def check_default(self):
        if self.search_count([('is_default', '=', True)]) > 1:
            raise UserError(_("You can't have more than one default config."))
