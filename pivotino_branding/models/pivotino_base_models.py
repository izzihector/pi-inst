from odoo import models, fields, api, _


class BaseModelExtend(models.AbstractModel):
    _name = 'basemodel.extend'

    # Remove Odoo wordings from help view
    def _register_hook(self):
        origin_get_empty = models.AbstractModel.get_empty_list_help

        @api.model
        def get_empty_list_help(self, help):
            res = origin_get_empty(self, help)
            if res:
                if 'Odoo' in res:
                    res = res.replace('Odoo', 'Pivotino')
            return res

        models.AbstractModel.get_empty_list_help = get_empty_list_help
        return super(BaseModelExtend, self)._register_hook()
