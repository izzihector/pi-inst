# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class PivotinoPreConfiguredData(models.Model):
    _name = "pivotino.preconfigured.data"
    _description = "Pre-Configured Data"

    name = fields.Char(string='Name')
    industry = fields.Many2one('pivotino.industry', string='Industry Name')
    leads_due_day = fields.Integer(string='Leads Due Day(s)')
    days_before_lead_lost = fields.Integer(string='Day(s) Before Lead Lost')
    target_sales = fields.Float(string='Target Sales')
    num_of_employees = fields.Integer(string='Number of Employee(s)')
