# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class LostReasonCategory(models.Model):
    _name = 'crm.lost.reason.category'
    _description = 'Opp. Lost Reason Category'

    name = fields.Char(string='Name', required=True)
    lost_reason_ids = fields.One2many('crm.lost.reason',
                                      'reason_category_id',
                                      string='Lost Reasons')


class LostReason(models.Model):
    _inherit = "crm.lost.reason"
    _order = "reason_category_id"

    reason_category_id = fields.Many2one('crm.lost.reason.category',
                                         string='Reason Category')


class CrmLeadLost(models.TransientModel):
    _inherit = 'crm.lead.lost'

    def get_display_message(self):
        """ Show warning message in the wizard form view if the leads have any
        quotation.
        """
        display_message = ''
        leads = self.env['crm.lead'].browse(self.env.context.get('active_ids'))
        # check if the leads has any quotation
        has_quotation = len([order for lead in leads
                             for order in lead.order_ids
                             if order.state in ('draft', 'sent')])
        if has_quotation:
            for lead in leads:
                if lead.order_ids:
                    display_message += \
                        _('<b>%s</b> has <b>%s</b> Quotations.<br/>') % \
                        (lead.name, len(lead.order_ids.filtered(
                            lambda x: x.state in ['draft', 'sent'])))
            display_message += _(
                '<br/>Marking this lead as lost will cancel the quotations. '
                'Do you want to proceed?<br>If yes, kindly select a lost '
                'reason for the Leads.')
        else:
            display_message += _('Kindly select a lost reason for the Leads.')
        return display_message

    display_message = fields.Text(default=get_display_message)

    def action_lost_reason_apply(self):
        """ Users are not allowed to mark any Lost Lead to Lost stage again.
        """
        leads = self.env['crm.lead'].browse(self.env.context.get('active_ids'))
        lost_leads = [lead.name for lead in leads if lead.is_lost]
        if lost_leads:
            raise ValidationError(_('You are not allowed to mark Lost Lead to '
                                    'lost:\n%s') % '\n'.join(lost_leads))
        return super(CrmLeadLost, self).action_lost_reason_apply()
