# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    auto_lead = fields.Boolean(string='Create Lead?',
                               default=lambda self: self.env.company.auto_lead)
    company_currency_id = fields.Many2one(related='company_id.currency_id',
                                          string='Company Currency')
    amount_total_base = fields.Monetary(compute='_compute_amount_total_base',
                                        string='Total', store=True,
                                        currency_field='company_currency_id',
                                        readonly=True)
    origin = fields.Char(copy=False)
    opportunity_id = fields.Many2one(copy=False)

    @api.depends('amount_total')
    def _compute_amount_total_base(self):
        """ Compute the amount_total in base currency """
        for order in self:
            company_currency = order.company_currency_id or \
                               self.env.company.currency_id
            amount_total_base = order.currency_id._convert(
                order.amount_total, company_currency, order.company_id,
                order.date_order or fields.Date.today())
            order.update({
                'amount_total_base': amount_total_base,
            })

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for sale in self:
            if sale.state == 'sale':
                sale.opportunity_id.stage_id = self.env.ref('pivotino_crm.stage_lead5')
        return res

    def write(self, values):
        res = super(SaleOrder, self).write(values)
        # if the opportunity is created from SO
        # when currency or order line is modified during draft state
        # update the opportunity
        if self.opportunity_id.is_from_so and self.state == 'draft':
            if values.get('currency_id') or values.get('order_line'):
                self.opportunity_id.lead_currency = self.currency_id
                self.opportunity_id.planned_revenue_input = self.amount_total
        return res

    @api.model
    def create(self, values):
        res = super(SaleOrder, self).create(values)
        default_opportunity_id = self.env.context.get('default_opportunity_id')
        won = self.env['crm.stage'].search([('is_won', '=', True)])
        lost = self.env['crm.stage'].search([('is_lost', '=', True)])
        quotation_stage = self.env['crm.stage'].search(
            [('is_quotation', '=', True)])
        if default_opportunity_id:
            opportunity = self.env['crm.lead'].search([('id', '=', default_opportunity_id)])
            if opportunity and len(opportunity.order_ids) <= 1:
                if opportunity.stage_id not in (won, lost):
                    opportunity.stage_id = quotation_stage.id
        # if the SO has auto_lead checked and not linked to any opportunity
        # (which mean the SO is manually created and not from a lead),
        # then create a new opportunity
        if res.auto_lead and not res.opportunity_id:
            opportunity_obj = self.env['crm.lead']
            opportunity_id = opportunity_obj.create({
                'name': res.name,
                'partner_id': res.partner_id.id,
                'user_id': res.user_id.id,
                'team_id': opportunity_obj._default_team_id(res.user_id.id).id,
                'stage_id': quotation_stage.id,
                'type': 'opportunity',
                'lead_currency': res.currency_id.id,
                'planned_revenue_input': res.amount_total,
                'is_from_so': True,
            })
            res.opportunity_id = opportunity_id.id
        return res

    @api.constrains('user_id')
    def check_same_salesperson(self):
        """ Ensure the salesperson field are same in SO and Lead
        """
        for order in self:
            if order.user_id and order.opportunity_id and \
                    order.opportunity_id.user_id:
                order_salesperson = order.user_id.id
                lead_salesperson = order.opportunity_id.user_id.id
                if order_salesperson != lead_salesperson:
                    raise ValidationError(_('You cannot have different '
                                            'Sales Person in Lead and SO. \n'
                                            'Kindly change the Sales Person '
                                            'in Lead.'))

    @api.constrains('partner_id')
    def check_same_customer(self):
        """ Ensure the customer field are same in SO and Lead
        """
        for order in self:
            if order.partner_id and order.opportunity_id and \
                    order.opportunity_id.partner_id:
                order_customer = order.partner_id.id
                lead_customer = order.opportunity_id.partner_id.id
                if order_customer != lead_customer:
                    raise ValidationError(_('You cannot have different '
                                            'Customer in Lead and SO. \n'
                                            'Kindly change the Customer in '
                                            'Lead.'))

    def action_cancel(self):
        """ Cancel all quotation of a lead will set the lead to lost.
        """
        from_lost_reason = self.env.context.get('from_lost_reason')
        # if this function is not called from the lost reason wizard and
        # the quotation is related to a lead
        if not from_lost_reason and self.opportunity_id:
            # get all the linked quotations
            lead_quotations = self.opportunity_id.order_ids.filtered(
                lambda m: m.id != self.id)
            # if no quotation left or all quotations are in 'cancel' state,
            # then ask for lost reason.
            if not lead_quotations or \
                    all(quote.state == 'cancel' for quote in lead_quotations):
                lead_quotation_form = \
                    self.env.ref('pivotino_crm.crm_lead_lost_quotation_form')
                ctx = {
                    'lead_id': self.opportunity_id.id,
                    'quotation_id': self.id,
                }
                # open a wizard to select Lost Reason
                return {
                    'name': _('Lead Lost Reason'),
                    'type': 'ir.actions.act_window',
                    'view_mode': 'form',
                    'res_model': 'crm.lead.lost.quotation',
                    'views': [(lead_quotation_form.id, 'form')],
                    'view_id': lead_quotation_form.id,
                    'target': 'new',
                    'context': ctx,
                }
        return super(SaleOrder, self).action_cancel()

