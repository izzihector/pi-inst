import base64

from odoo import models, fields, modules, api, _


class Channel(models.Model):
    _inherit = 'mail.channel'

    # override to change the default channel image
    def _get_default_image(self):
        image_path = modules.get_module_resource(
            'pivotino_branding_mail', 'static/src/img', 'groupdefault.png')
        return base64.b64encode(open(image_path, 'rb').read())

    image_128 = fields.Image(default=_get_default_image)
