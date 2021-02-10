# -*- coding: utf-8 -*-
# Using in future for cron job
from odoo import api, fields, models, _
from odoo.exceptions import UserError
import json


class GeneralFeedbackTags(models.Model):
    _name = "general.feedback.tags"
    _description = "General Feedbacks Tags"

    value = fields.Char(string='Tag Value')
    type = fields.Selection([('positive', 'Positive'), ('negative', 'Negative')],
        string='Kanban State',)
    assigned = fields.Boolean(string='Currently in Used', copy=False,
                              default=False)
    code = fields.Char(string='Code', copy=False)

    @api.constrains('assigned')
    def _check_number_of_assigned(self):
        if self.search_count([('type', '=', 'positive'),('assigned', '=', True)]) > 6:
            raise UserError(_("You can't have more than six assigned positive tags."))

        if self.search_count([('type', '=', 'negative'),('assigned', '=', True)]) > 6:
            raise UserError(_("You can't have more than six assigned negative tags."))

    @api.model
    def get_tags_object(self):
        positive = self.search([('type', '=', 'positive'), ('assigned', '=', True)])
        negative = self.search([('type', '=', 'negative'), ('assigned', '=', True)])

        pos_final_list = []
        neg_final_list = []
        pos_list = []
        neg_list = []
        for pos in positive:
            pos_list.append({
                'code': pos.code,
                'value': pos.value})
            if len(pos_list) == 2:
                pos_final_list.append(pos_list)
                pos_list = []
        for neg in negative:
            neg_list.append({
                'code': neg.code,
                'value': neg.value})
            if len(neg_list) == 2:
                neg_final_list.append(neg_list)
                neg_list = []
        return pos_final_list, neg_final_list
