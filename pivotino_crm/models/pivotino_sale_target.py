# -*- coding: utf-8 -*-

import pytz
from calendar import monthrange
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def convert_timezone(from_tz, to_tz, dt):
    from_tz = pytz.timezone(from_tz).localize(
        datetime.strptime(dt, DATETIME_FORMAT))
    to_tz = from_tz.astimezone(pytz.timezone(to_tz))
    return to_tz.strftime(DATETIME_FORMAT)


month_list = [
    ('1', 'January'),
    ('2', 'February'),
    ('3', 'March'),
    ('4', 'April'),
    ('5', 'May'),
    ('6', 'June'),
    ('7', 'July'),
    ('8', 'August'),
    ('9', 'September'),
    ('10', 'October'),
    ('11', 'November'),
    ('12', 'December'),
]


def get_month_selection():
    return month_list


class SaleTarget(models.Model):
    _name = 'sale.target'
    _description = 'Sale Target of Company'
    _order = 'target_year desc, target_month desc'

    name = fields.Char(compute='_compute_name',
                       string='Target Reference',
                       required=True,
                       copy=False,
                       readonly=True,
                       store=True,
                       default=lambda self: _('New'))
    company_id = fields.Many2one('res.company',
                                 string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)
    target_month = fields.Selection(get_month_selection(),
                                    string='Month',
                                    default=False,
                                    copy=False)
    target_year = fields.Char(string='Year', required=True, size=4,
                              default=lambda s: fields.Datetime.now().year,
                              copy=False)
    target_date = fields.Date(compute='_compute_target_date',
                              string='Target Date',
                              copy=False,
                              store=True)
    target_amount = fields.Float(compute='_compute_target_actual_amount',
                                 string='Target Amount',
                                 store=True)
    actual_amount = fields.Float(compute='_compute_target_actual_amount',
                                 string='Actual Amount',
                                 store=True)
    individual_ids = fields.One2many('sale.target.individual',
                                     'target_id',
                                     string='Targets and Actual',
                                     copy=True)

    _sql_constraints = [
        ('target_month_year_uniq',
         'unique(company_id,target_month,target_year)',
         'Sales target of this month is already set in this company.')
    ]

    @api.constrains('target_year')
    def _check_year_size(self):
        """ Check the year input validity
        """
        for target in self:
            year = target.target_year
            # raise Error when the year size is not equal to 4 and not a digit
            if year and (len(year) != 4 or not year.isdigit()):
                raise ValidationError(_('Invalid Year!'))

    @api.depends('target_month', 'target_year')
    def _compute_name(self):
        """ Generate the name based on the month and the year
        """
        for target in self:
            if target.target_month and target.target_year:
                target.name = '%s %s' % (
                    month_list[int(target.target_month)-1][1],
                    target.target_year)

    @api.depends('target_month', 'target_year')
    def _compute_target_date(self):
        """ Generate the date based on the month and the year
        """
        for target in self:
            if target.target_month and target.target_year:
                target.target_date = datetime(int(target.target_year),
                                              int(target.target_month),
                                              15)

    @api.depends('individual_ids', 'individual_ids.target_sales',
                 'individual_ids.actual_sales', 'company_id')
    def _compute_target_actual_amount(self):
        """ Compute the target amount and actual amount for the month target
        """
        for target in self:
            target.target_amount = False
            target.actual_amount = False
            # get the individual lines
            if target.individual_ids:
                # sum the target amount of individuals
                target.target_amount = sum(
                    [individual.target_sales
                     for individual in target.individual_ids])
                # sum the actual amount of individuals
                target.actual_amount = sum(
                    [individual.actual_sales
                     for individual in target.individual_ids])

    @api.model
    def _auto_create_sale_target(self):
        # get companies
        for company in self.env['res.company'].search([]):
            # get the next month
            next_month = fields.Datetime.now() + relativedelta(months=1)
            year = next_month.year
            month = str(next_month.month)
            sale_target_obj = self.env['sale.target']
            # search if any existing record matches next month target
            exist_sale_target = sale_target_obj.search([
                ('company_id', '=', company.id),
                ('target_year', '=', year),
                ('target_month', '=', month)], limit=1)
            if exist_sale_target:
                continue
            # get the latest record of sale target
            last_sale_target = sale_target_obj.search([
                ('company_id', '=', company.id)],
                order='target_year desc, target_month desc',
                limit=1)
            # if last_sale_target, copy a new Sale Target
            if last_sale_target:
                last_sale_target.copy({
                    'target_year': year,
                    'target_month': month
                })
            # create a sale target using default sale target
            else:
                sale_target_obj.create({
                    'company_id': company.id,
                    'target_year': year,
                    'target_month': month,
                    'target_amount': company.default_sale_target
                })


class SaleTargetIndividual(models.Model):
    _name = 'sale.target.individual'
    _description = 'Sale Target of Individual'

    target_id = fields.Many2one('sale.target',
                                string='Parent Target',
                                required=True,
                                ondelete='cascade')
    company_id = fields.Many2one(related='target_id.company_id',
                                 string='Company',
                                 store=True,
                                 readonly=True)
    user_id = fields.Many2one('res.users',
                              string='Sales Person',
                              required=True)
    target_month = fields.Selection(related='target_id.target_month',
                                    string='Target Month')
    target_year = fields.Char(related='target_id.target_year',
                              string='Target Year')
    target_date = fields.Date(related='target_id.target_date',
                              string='Target Date')
    target_sales = fields.Float(string='Target')
    actual_sales = fields.Float(compute='_compute_actual_sales',
                                string='Actual',
                                store=True,
                                copy=False)
    variance = fields.Float(compute='_compute_variance',
                            string='Variance',
                            store=True,
                            copy=False)

    @api.depends('user_id', 'user_id.sale_ids', 'target_year', 'target_month',
                 'user_id.sale_ids.amount_total', 'user_id.sale_ids.state')
    def _compute_actual_sales(self):
        """ Compute the actual sales of the user
        """
        for individual in self:
            individual.actual_sales = 0
            if individual.target_id.target_year and \
                    individual.target_id.target_month:
                target_year = int(individual.target_id.target_year)
                target_month = int(individual.target_id.target_month)
                month_range = monthrange(target_year, target_month)
                first_day = datetime(target_year, target_month, 1, 0, 0, 0)
                last_day = datetime(target_year, target_month, month_range[1],
                                    23, 59, 59)
                first_day = convert_timezone('UTC',
                                             individual.user_id.tz or 'UTC',
                                             datetime.strftime(
                                                 first_day, DATETIME_FORMAT))
                last_day = convert_timezone('UTC',
                                            individual.user_id.tz or 'UTC',
                                            datetime.strftime(
                                                last_day, DATETIME_FORMAT))
                if individual.user_id:
                    # get the sale order amount total in particular month
                    sale_orders = self.env['sale.order'].search([
                        ('user_id', '=', individual.user_id.id),
                        ('date_order', '>=',
                         datetime.strptime(first_day, DATETIME_FORMAT)),
                        ('date_order', '<=',
                         datetime.strptime(last_day, DATETIME_FORMAT)),
                        ('state', 'in', ['sale', 'done'])
                    ])
                    if sale_orders:
                        individual.actual_sales = sum([
                            sale_order.amount_total
                            for sale_order in sale_orders
                        ])

    @api.depends('target_sales', 'actual_sales')
    def _compute_variance(self):
        """ Compute the variance between target sales and actual sales.
        If the actual sales > target sales, make the variance as 0
        """
        for individual in self:
            variance = individual.target_sales - individual.actual_sales
            if variance > 0:
                individual.variance = variance
            else:
                individual.variance = 0
