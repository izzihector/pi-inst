from odoo import models, fields, api, _
from odoo import tools
from odoo.exceptions import UserError
from datetime import datetime
import requests
import logging
import re

_logger = logging.getLogger(__name__)


class Users(models.Model):
    _inherit = 'res.users'

    is_hide_access = fields.Boolean(string='Hide Setting Access Right Tab',
                                    default=True)
    user_role = fields.Selection([
        ('user', 'User'),
        ('owner', 'Business Owner'),
    ], string='User Role', default=False)
    cust_email_creation = fields.Boolean(string="cPanel Email Creation Successfull?",
                                         default=False, readonly=True)
    customer_client_id = fields.Integer(string="Customer ID", default=0,
                                        readonly=True)
    is_admin = fields.Boolean(string='Is Admin', default=False)
    main_user = fields.Boolean(string="Owner of Database", default=False,
                               readonly=True)
    client_domain = fields.Char(string='Domain', readonly=True, copy=False)
    # disable the pivotino bot chat temporarily for first launch
    odoobot_state = fields.Selection(default="disabled")

    @api.constrains('login')
    def _check_login_email_format(self):
        if self.login and not tools.single_email_re.match(self.login):
            raise UserError(_("You have entered an invalid e-mail address. "
                              "Please try again."))

    @api.model
    def install_l10n_coa_module(self, name):
        ir_module = self.env['ir.module.module']
        ir_module.update_list()
        coa_module = ir_module.search([('state', '!=', 'installed'),
                                       ('name', '=', name)], limit=1)
        if coa_module:
            coa_module.button_immediate_install()
        else:
            generic_module = ir_module.search([
                ('state', '!=', 'installed'),
                ('name', '=', 'pivotino_l10n_generic_coa')], limit=1)
            if generic_module:
                generic_module.button_immediate_install()
        return True

    @api.model_create_multi
    def create(self, vals_list):
        # get business owner group and user group
        group_user = self.env.ref('pivotino_base.group_pivotino_user')
        group_owner = self.env.ref('pivotino_base.group_pivotino_owner')

        # admin access right
        group_erp_manager = self.env.ref('base.group_erp_manager')

        users = super(Users, self).create(vals_list)
        for vals in vals_list:
            if vals.get('login', False):
                domain = re.search("@yahoo", vals['login'])
                if domain:
                    raise UserError(_('Currently our system does not support Yahoo domain for emails!'))
        for user in users:
            # on create, assign user to their respective group
            if user.user_role == 'user':
                # assign user group
                group_user.sudo().write({'users': [(4, user.id)]})
            elif user.user_role == 'owner':
                # assign admin group
                group_erp_manager.sudo().write({'users': [(4, user.id)]})

                # assign user and owner group
                group_user.sudo().write({'users': [(4, user.id)]})
                group_owner.sudo().write({'users': [(4, user.id)]})

            # update analytic tracking user count
            user_count_rec = self.env.ref('pivotino_base.analytic_users_count')
            user_count_rec.tracking_record_increment_integer(1)
        return users

    def write(self, vals):
        # get view access group
        access_group = self.env.ref('pivotino_base.group_view_access')

        # get business owner group and user group
        group_owner = self.env.ref('pivotino_base.group_pivotino_owner')

        # admin access right
        group_erp_manager = self.env.ref('base.group_erp_manager')

        # assign and remove access right group to user
        if vals and 'is_hide_access' in vals:
            if vals.get('is_hide_access') is True:
                if self.env.uid in access_group.users.ids:
                    access_group.write({'users': [(3, self.env.uid)]})
            else:
                if self.env.uid not in access_group.users.ids:
                    access_group.write({'users': [(4, self.env.uid)]})

        # update user role in res users then update groups
        if vals and 'user_role' in vals:
            if vals.get('user_role') == 'user' and \
                    self.has_group('pivotino_base.group_pivotino_owner'):
                # demote from owner to user
                group_erp_manager.sudo().write({'users': [(3, self.id)]})

                group_owner.sudo().write({'users': [(3, self.id)]})
                for group in group_owner.implied_ids:
                    group.sudo().write({'users': [(3, self.id)]})
            elif vals.get('user_role') == 'owner' and not \
                    self.has_group('pivotino_base.group_pivotino_owner'):
                # promote from user to owner
                group_erp_manager.sudo().write({'users': [(4, self.id)]})

                group_owner.sudo().write({'users': [(4, self.id)]})
        res = super(Users, self).write(vals)

        # restrict yahoo emails
        for user in self:
            if user.login:
                domain = re.search("@yahoo", user.login)
                if domain:
                    raise UserError(_(
                        'Currently our system does not support Yahoo domain for emails!'))

        return res

    def _cron_create_cPanel_email(self):
        failed_users = self.search([('cust_email_creation', '=', False), ('main_user', '=', True)])
        for user in failed_users:
            user_name = user.name
            if user_name:
                try:
                    url = 'http://customer.pivotino.com/cpanel_api.php'
                    data = [('1', user_name)]
                    respond = requests.post(url, data=data)
                    if respond.text == '1':
                        user.cust_email_creation = True
                        vals = {
                            'name': 'Outgoing Mail',
                            'smtp_host': 'customer.pivotino.com',
                            'smtp_encryption': 'starttls',
                            'smtp_port': 587,
                            'smtp_user': user_name + '@customer.pivotino.com',
                            'smtp_pass': 'gE1(Re@t|Ve',
                        }
                        self.env['ir.mail_server'].create(vals)
                except Exception:
                    pass
        return True

    @api.model
    def insert_preconfigured_data_from_provision(
            self, user_id, domain, url, customer_client_id):
        user = self.sudo().search([('id', '=', user_id)])
        if user:
            user_country = user.country_id
            currency = user_country.currency_id

            if currency:
                if currency.active == False:
                    currency.sudo().write({
                        'active': True
                    })

            # write pricelist into partner
            if user_country:
                pricelist = self.env['product.pricelist'].sudo().search(
                    [('currency_id', '=', currency.id)])
                user.partner_id.property_product_pricelist = pricelist

        catchall_alias = self.env.ref('mail.icp_mail_catchall_alias')
        bounce_alias = self.env.ref('mail.icp_mail_bounce_alias')

        if domain:
            catchall_alias.sudo().write({
                'value': domain,
            })
            bounce_alias.sudo().write({
                'value': domain,
            })

        if url:
            self.env['ir.config_parameter'].sudo().set_param(
                'web.base.url', url)

        first_login_track_user = self.env['ir.config_parameter']
        str_id = str(customer_client_id)
        first_login_track_user.sudo().set_param('first.login.track.user', str_id)
        return True
