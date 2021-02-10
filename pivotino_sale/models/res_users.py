from odoo import models, fields, api, _


class Users(models.Model):
    _inherit = 'res.users'

    @api.model_create_multi
    def create(self, vals_list):
        # billing and billing administrator group
        group_account_manager = self.env.ref('account.group_account_manager')
        group_account_invoice = self.env.ref('account.group_account_invoice')

        # sales admin and sales lead
        group_sale_manager = self.env.ref('sales_team.group_sale_manager')
        group_sale_lead = self.env.ref(
            'sales_team.group_sale_salesman_all_leads')

        users = super(Users, self).create(vals_list)
        for user in users:
            # remove all invoicing groups
            if user.has_group('account.group_account_manager') and \
                    user.has_group('account.group_account_invoice'):
                group_account_manager.sudo().write({'users': [(3, user.id)]})
                group_account_invoice.sudo().write({'users': [(3, user.id)]})

            # remove sales admin group
            if user.has_group('sales_team.group_sale_manager'):
                group_sale_manager.sudo().write({'users': [(3, user.id)]})

            if user.user_role == 'user':
                # remove sale lead group
                group_sale_lead.sudo().write({'users': [(3, user.id)]})
        return users

    def write(self, vals):
        # sale lead group
        group_sale_lead = self.env.ref(
            'sales_team.group_sale_salesman_all_leads')

        if vals and 'user_role' in vals:
            if vals.get('user_role') == 'user' and \
                    self.has_group('pivotino_base.group_pivotino_owner'):
                group_sale_lead.sudo().write({'users': [(3, self.id)]})
            elif vals.get('user_role') == 'owner' and not \
                    self.has_group('pivotino_base.group_pivotino_owner'):
                group_sale_lead.sudo().write({'users': [(4, self.id)]})
        return super(Users, self).write(vals)
