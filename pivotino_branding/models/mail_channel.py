from odoo import models, fields, api, _


class Channel(models.Model):
    _inherit = 'mail.channel'

    # Override for debranding
    @api.model
    def init_odoobot(self):
        if self.env.user.odoobot_state == 'not_initialized':
            partner = self.env.user.partner_id
            odoobot_id = self.env['ir.model.data'].xmlid_to_res_id(
                "base.partner_root")
            channel = self.with_context(mail_create_nosubscribe=True).create({
                'channel_partner_ids': [(4, partner.id), (4, odoobot_id)],
                'public': 'private',
                'channel_type': 'chat',
                'email_send': False,
                'name': 'PivotinoBot'
            })
            message = _(
                "Hello,<br/>Pivotino's chat helps employees collaborate efficiently. I'm here to help you discover its features.<br/><b>Try to send me an emoji :)</b>")
            channel.sudo().message_post(body=message, author_id=odoobot_id,
                                        message_type="comment",
                                        subtype="mail.mt_comment")
            self.env.user.odoobot_state = 'onboarding_emoji'
            return channel
