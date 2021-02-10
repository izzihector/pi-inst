from odoo import models, fields, api, _


class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    def _get_creation_message(self):
        # default will get model name but crm.lead model name=Lead/Opportunity
        # check if crm.lead then return "Opportunity created"
        if self._name == 'crm.lead':
            return _('Opportunity created')
        else:
            return super(MailThread, self)._get_creation_message()
