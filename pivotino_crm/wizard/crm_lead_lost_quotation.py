# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class CrmLeadLostQuotation(models.TransientModel):
    _name = 'crm.lead.lost.quotation'
    _description = 'Get Lost Reason of Lead from Quotations'

    lost_reason_id = fields.Many2one('crm.lost.reason',
                                     'Lost Reason',
                                     required=True)

    def action_lost_reason_quotation_reply(self):
        """ Get the lost reason from quotation form view and make the lead as
        lost.
        """
        # get the lead
        lead = self.env['crm.lead'].browse(self.env.context.get('lead_id'))
        # get the quotation
        quotation = self.env['sale.order'].browse(
            self.env.context.get('quotation_id'))
        # make the lead as lost
        lead.action_set_lost(lost_reason=self.lost_reason_id.id)
        # call the action_cancel for the quotation
        return quotation.with_context(from_lost_reason=True).action_cancel()
