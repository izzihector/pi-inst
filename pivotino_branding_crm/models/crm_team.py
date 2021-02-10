# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class Team(models.Model):
    _inherit = 'crm.team'

    @api.model
    def action_your_pipeline(self):
        """ Inherit this function to replace Odoo with Pivotino in help content
        when the current login user doesn't belong to any sales team
        """
        res = super(Team, self).action_your_pipeline()
        if res.get('help'):
            if ' Odoo ' in res['help']:
                res['help'] = res['help'].replace(' Odoo ', ' Pivotino ')
        return res
