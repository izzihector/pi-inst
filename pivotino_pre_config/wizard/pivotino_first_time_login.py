# -*- coding: utf-8 -*-

import pytz
from datetime import datetime
from odoo import models, fields, api, _
import pycountry
from forex_python.converter import CurrencyCodes
import xmlrpc.client
import ssl

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def convert_timezone(from_tz, to_tz, dt):
    from_tz = pytz.timezone(from_tz).localize(
        datetime.strptime(dt, DATETIME_FORMAT))
    to_tz = from_tz.astimezone(pytz.timezone(to_tz))
    return to_tz


class FirstTimeLogin(models.TransientModel):
    _name = "first.time.login"
    _description = 'First Time Login'

    industry = fields.Many2one('pivotino.industry', string='Industry')
    is_other_industry = fields.Boolean(string='Is Other Industry?')
    industry_others = fields.Text(string="Others")
    leads_due_day = fields.Selection([('2', "2"), ('7', "7"), ('14', "14"), ('other', "Others")],
                                     string="Leads Due Day")
    due_day_others = fields.Integer(string="Others")
    days_before_lead_lost = fields.Selection([('7', "7"), ('14', "14"), ('30', "30"), ('other', "Others")],
                                             string="Lost Leads Due Day")
    days_before_lead_lost_others = fields.Integer(string="Others")
    target_sales = fields.Float(string='Target Sales')
    num_of_employees = fields.Selection([('1', "1"), ('2', "2"), ('5', "5"), ('other', "Others")],
                                        string="Number of Employee(s)")
    num_of_employees_other = fields.Integer(string='Others')

    @api.onchange('industry')
    def onchange_is_other_industry(self):
        if self.industry.is_others:
            self.is_other_industry = True
        else:
            self.is_other_industry = False

    def update_pre_configured_data(self):
        configured_data = self.env['pivotino.preconfigured.data'].create({
            'name': 'First Time Login'
        })

        if self.industry:
            if self.industry.is_others and self.industry_others:
                other_industry = self.env['pivotino.industry'].create({'name': self.industry_others})
                configured_data.industry = other_industry.id
                self.env.user.company_id.industry = other_industry.id
            else:
                configured_data.industry = self.industry.id
                self.env.user.company_id.industry = self.industry.id

        if self.leads_due_day:
            if self.leads_due_day == 'other':
                configured_data.leads_due_day = self.due_day_others
                self.env.user.company_id.day_set_due = self.due_day_others
                # call onchange to update all due date of all activity type
                self.env.user.company_id.change_activity_date()
            else:
                configured_data.leads_due_day = int(self.leads_due_day)
                self.env.user.company_id.day_set_due = int(self.leads_due_day)
                # call onchange to update all due date of all activity type
                self.env.user.company_id.change_activity_date()

        if self.days_before_lead_lost:
            if self.days_before_lead_lost == 'other':
                configured_data.days_before_lead_lost = self.days_before_lead_lost_others
                self.env.user.company_id.day_set_lost = self.days_before_lead_lost_others
            else:
                configured_data.days_before_lead_lost = int(self.days_before_lead_lost)
                self.env.user.company_id.day_set_lost = int(self.days_before_lead_lost)

        # To do: Populate data to specific pre-configured fields after development ( Zen )
        # create sale target record
        today = datetime.now()
        utc_today_string = today.strftime("%Y-%m-%d %H:%M:%S")
        tz_today_string = convert_timezone('UTC',
                                           self.env.user.tz or 'UTC',
                                           utc_today_string)
        sale_target_obj = self.env['sale.target']
        sale_target_obj.create({
            'company_id': self.env.user.company_id.id,
            'target_month': str(tz_today_string.month),
            'target_year': tz_today_string.year,
            'individual_ids': [(0, 0, {
                'user_id': self.env.user.id,
                'target_sales': self.target_sales or 0,
            })],
        })
        # write the target_sales to the company default sales target
        if self.target_sales:
            configured_data.target_sales = self.target_sales
            self.env.company.default_sale_target = self.target_sales

        # user_country = self.env.user.country_id
        # currency = user_country.currency_id
        #
        # if currency:
        #     if currency.active == False:
        #         currency.active = True
        #
        # # write pricelist into partner
        # if user_country:
        #     pricelist = self.env['product.pricelist'].search([('currency_id', '=', currency.id)])
        #     self.env.user.partner_id.property_product_pricelist = pricelist
        #
        # catchall_alias = self.env.ref('mail.icp_mail_catchall_alias')
        # bounce_alias = self.env.ref('mail.icp_mail_bounce_alias')
        #
        # if self.env.user.client_domain:
        #     catchall_alias.sudo().write({
        #         'value': self.env.user.client_domain,
        #     })
        #     bounce_alias.sudo().write({
        #         'value': self.env.user.client_domain,
        #     })

        # # Call Portal API and write into res.users when user first logged in
        # api_config = self.env['api.configuration'].search([
        #     ('is_default', '=', True)
        # ], limit=1)
        # url = api_config.url
        # db = api_config.db_name
        # username = api_config.username
        # password = api_config.password
        # common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url),
        #                                    verbose=False,
        #                                    context=ssl._create_unverified_context())
        # uid = False
        # while not uid:
        #     uid = common.authenticate(db, username, password, {})
        # models = xmlrpc.client.ServerProxy(
        #     '{}/xmlrpc/2/object'.format(url), verbose=False,
        #     context=ssl._create_unverified_context())
        # models.execute_kw(db, uid, password, 'res.users', 'track_first_login',
        #                   [self.env.user.customer_client_id])

        self.env.user._update_last_login()

        if self.env.user.sudo().user_role == 'user':
            action = self.env.ref('pivotino_pre_config.action_starter_wizard_sales').read()[0]
        else:
            action = self.env.ref('pivotino_pre_config.action_starter_wizard_business').read()[0]
        return action
