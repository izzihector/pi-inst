from odoo import models, fields, api, _
from odoo.exceptions import UserError
import re


class Partner(models.Model):
    _inherit = "res.partner"

    is_admin = fields.Boolean(string='Is Admin', default=False)
    company_type = fields.Selection(
        selection=[('company', 'Company'), ('person', 'Individual')]
    )

    @api.model
    def get_import_templates(self):
        return [{
            'label': _('Import Template for Customers'),
            'template': '/pivotino_base/static/xls/res_partner.xls'
        }]

    @api.model
    def create(self, vals):
        res = super(Partner, self).create(vals)

        # update analytic tracking contact count
        contact_count_rec = self.env.ref(
            'pivotino_base.analytic_contact_count')
        contact_count_rec.tracking_record_increment_integer(1)

        # restrict yahoo emails
        if vals.get('email', False):
            domain = re.search("@yahoo", vals['email'])
            if domain:
                raise UserError(_('Currently our system does not support Yahoo domain for emails!'))
        return res

    def write(self, vals):
        res = super(Partner, self).write(vals)

        # restrict yahoo emails
        for user in self:
            if user.email:
                domain = re.search("@yahoo", user.email)
                if domain:
                    raise UserError(_(
                        'Currently our system does not support Yahoo domain for emails!'))
        return res


class MailMail(models.Model):
    _inherit = 'mail.mail'

    @api.model
    def create(self, values):
        print('values -------------->', values)
        res = super(MailMail, self).create(values)
        return res
