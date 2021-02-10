# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class StarterWizard(models.TransientModel):
    _name = 'starter.wizard'
    _description = 'Welcome to PIVOTINO'

    dashboard_url = fields.Char()

    def button_next(self):
        action = {
            'name' : 'Welcome To PIVOTINO',
            'res_model' : 'starter.wizard',
            'type' : 'ir.actions.act_window',
            'view_id': self.env.ref('pivotino_pre_config.starter_wizard_view_video_bo').id,
            'view_mode' : 'form',
            'target' : 'new'
        }
        return action
    
    def button_dashboard(self):
        action = {
            'name' : 'Dashboard Quick Review',
            'res_model' : 'starter.wizard',
            'type' : 'ir.actions.act_window',
            'view_id': self.env.ref('pivotino_pre_config.dashboard_wizard_view').id,
            'view_mode' : 'form',
            'target' : 'new'
        }
        return action

    def button_so_video(self):
        action = {
            'name' : 'Welcome To PIVOTINO',
            'res_model' : 'starter.wizard',
            'type' : 'ir.actions.act_window',
            'view_id': self.env.ref('pivotino_pre_config.starter_wizard_view_video').id,
            'view_mode' : 'form',
            'target' : 'new'
        }
        return action

    def show_video(self):
        # update analytic tracking dashboard video view count
        dashboard_video_view_count_rec = self.env.ref(
            'pivotino_pre_config.analytic_dashboard_video_count')
        dashboard_video_view_count_rec.tracking_record_increment_integer(1)

        video = self.env.context.get('video')
        all_views = {
            1: 'pivotino_pre_config.dashboard_video_1',
            2: 'pivotino_pre_config.dashboard_video_2',
            3: 'pivotino_pre_config.dashboard_video_3',
            4: 'pivotino_pre_config.dashboard_video_4',
            5: 'pivotino_pre_config.dashboard_video_5',
        }
        if all_views.get(video):
            view = self.env.ref(all_views.get(video))
        else:
            raise UserError(_('Sorry, Video is not available!'))
        action = {
            'name': 'Dashboard Quick Review',
            'res_model': 'starter.wizard',
            'type': 'ir.actions.act_window',
            'view_id': view.id,
            'view_mode': 'form',
            'target': 'new',
        }
        return action

    def button_done(self):
        # update analytic tracking starter kit view count
        starter_kit_count_rec = self.env.ref(
            'pivotino_pre_config.analytic_starter_kit_count')
        starter_kit_count_rec.tracking_record_increment_integer(1)

        self.sudo().env.user.clogin = True
        action = {
            'name' : 'Dashboard Quick Review',
            'res_model' : 'starter.wizard',
            'type' : 'ir.actions.act_window',
            'view_id': self.env.ref('pivotino_pre_config.dashboard_wizard_view').id,
            'view_mode' : 'form',
            'target' : 'new'
        }
        return action
