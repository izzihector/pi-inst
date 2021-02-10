# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class CrmTeam(models.Model):
    _inherit = 'crm.team'

    sales_target = fields.Integer(string='Sales Target')

    @api.model
    def action_your_pipeline(self):
        """
            inherit and change the help message with same condition
            because base message shows word "Sales Team"
        """
        action = super(CrmTeam, self).action_your_pipeline()
        user_team_id = self.env.user.sale_team_id.id
        if not user_team_id:
            action['help'] = _("""
                <p class='o_view_nocontent_smiling_face'>
                    Add new opportunities, see your business grow!
                </p>
                <p>
                    Get started by clicking on the "Create" button above
                    to add new opportunities.
                </p>
                <p>
                    You will be able to keep track of your pipeline and
                    convert them to sales.
                </p>
            """)
        return action
