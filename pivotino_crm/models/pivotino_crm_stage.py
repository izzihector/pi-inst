# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Stage(models.Model):
    _inherit = 'crm.stage'

    is_lost = fields.Boolean('Is Lost Stage?')
    is_quotation = fields.Boolean('Is Quotation Stage?')
    stage_sequence = fields.Integer('Stage Sequence',
                                    help="Used to order stages. Lower is better.",
                                    default=0)
    stage_duration_ids = fields.One2many('crm.stage.duration',
                                         'stage_id',
                                         string='Stage Durations')

    @api.constrains('is_lost', 'is_won')
    def constrain_won_lost_stage(self):
        for stage in self:
            print('HEREEEEEEEEEEE?')
            is_won_stage = self.search([('is_won', '=', True), ('id', '!=', stage.id)])
            is_lost_stage = self.search([('is_lost', '=', True), ('id', '!=', stage.id)])
            if stage.is_won and stage.is_lost:
                raise ValidationError(_('You cannot select both Won and Lost'))
            if stage.is_won and is_won_stage:
                print('NOT HEREEEEEEEEEEEEEEEEEEEE?')
                raise ValidationError(_('You can only have 1 stage for Won'))
            if stage.is_lost and is_lost_stage:
                raise ValidationError(_('You can only have 1 stage for Lost'))

    @api.constrains('is_quotation')
    def constrain_quotation_stage(self):
        quotation_stage = self.search([('is_quotation', '=', True), ('id', '!=', self.id)])
        if self.is_quotation and quotation_stage:
            raise ValidationError(_('There can only be 1 quotation stage!'))

    @api.constrains('stage_sequence')
    def check_stage_sequence_duplicate(self):
        for stage in self.search([]):
            stage_sequence = self.search([
                ('stage_sequence', '=', stage.stage_sequence),
                ('id', '!=', stage.id)
            ])
            if stage.stage_sequence and stage_sequence:
                raise ValidationError(_('This sequence is selected in another stage!'))

    @api.model
    def create(self, values):
        res = super(Stage, self).create(values)
        if res.stage_sequence == 0:
            res.update_sequence()
        return res

    def update_sequence(self):
        mylist = []
        for stage in self.search([]):
            mylist.append(stage.stage_sequence)
        self.stage_sequence = max(mylist) + 1
