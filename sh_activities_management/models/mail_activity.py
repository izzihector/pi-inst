# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models, fields, api
from odoo.http import request
import datetime

from odoo import http
from odoo.http import request
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class MailActivity(models.Model):
    """ Inherited Mail Acitvity to add custom field"""
    _inherit = 'mail.activity'
    
    active = fields.Boolean(default=True)
    supervisor_id = fields.Many2one('res.users',string="Supervisor")
    done = fields.Boolean(default=False)
    state = fields.Selection(selection_add=[("done", "Done")], compute="_compute_state",store=True)
    date_done = fields.Date("Completed Date", index=True, readonly=True)
    
    @api.depends("date_deadline", "done")
    def _compute_state(self):
        super()._compute_state()
        for record in self.filtered(lambda activity: activity.done):
            record.state = "done"
    
    def action_done(self):
        """ Wrapper without feedback because web button add context as
        parameter, therefore setting context to feedback """
        messages, next_activities = self._action_done()
        self.state='done'
        self.active=True
        self.date_done = fields.Date.today()
        return messages.ids and messages.ids[0] or False

    def _action_done(self, feedback=False, attachment_ids=None):
        """ Private implementation of marking activity as done: posting a message, deleting activity
            (since done), and eventually create the automatical next activity (depending on config).
            :param feedback: optional feedback from user when marking activity as done
            :param attachment_ids: list of ir.attachment ids to attach to the posted mail.message
            :returns (messages, activities) where
                - messages is a recordset of posted mail.message
                - activities is a recordset of mail.activity of forced automically created activities
        """
        # marking as 'done'
        messages = self.env['mail.message']
        next_activities_values = []
        for activity in self:
            # extract value to generate next activities
            if activity.force_next:
                Activity = self.env['mail.activity'].with_context(activity_previous_deadline=activity.date_deadline)  # context key is required in the onchange to set deadline
                vals = Activity.default_get(Activity.fields_get())

                vals.update({
                    'previous_activity_type_id': activity.activity_type_id.id,
                    'res_id': activity.res_id,
                    'res_model': activity.res_model,
                    'res_model_id': self.env['ir.model']._get(activity.res_model).id,
                })
                virtual_activity = Activity.new(vals)
                virtual_activity._onchange_previous_activity_type_id()
                virtual_activity._onchange_activity_type_id()
                next_activities_values.append(virtual_activity._convert_to_write(virtual_activity._cache))

            # post message on activity, before deleting it
            record = self.env[activity.res_model].browse(activity.res_id)
            record.message_post_with_view(
                'mail.message_activity_done',
                values={
                    'activity': activity,
                    'feedback': feedback,
                    'display_assignee': activity.user_id != self.env.user
                },
                subtype_id=self.env['ir.model.data'].xmlid_to_res_id('mail.mt_activities'),
                mail_activity_type_id=activity.activity_type_id.id,
                attachment_ids=[(4, attachment_id) for attachment_id in attachment_ids] if attachment_ids else [],
            )
            messages |= record.message_ids[0]

        next_activities = self.env['mail.activity'].create(next_activities_values)
#         self.unlink()  # will unlink activity, dont access `self` after that

        return messages, next_activities

class ActivityDashboard(models.Model):
    _name = 'activity.dashboard'
    _description = 'Activity Dashboard'

    
    @api.model
    def get_sh_crm_activity_planned_count_tbl(self,filter_date,filter_user,start_date,end_date,filter_supervisor):
        doman = []

        crm_days_filter = filter_date 
        custom_date_start = start_date
        custom_date_end = end_date 
        planned_activities_count = 0
        completed_activities_count = 0
        overdue_activities_count = 0        
        if crm_days_filter == 'today':
           
            dt_flt1 = []
            dt_flt1.append('date_deadline')
            dt_flt1.append('>=')
            dt_flt1.append(datetime.now().date().strftime("%Y/%m/%d"))
            doman.append( tuple(dt_flt1) )
             
            dt_flt2 = []
            dt_flt2.append('date_deadline')
            dt_flt2.append('<=')
            dt_flt2.append(datetime.now().date().strftime("%Y/%m/%d"))
            doman.append( tuple(dt_flt2) )
        elif crm_days_filter == 'yesterday':
           
            dt_flt1 = []
            dt_flt1.append('date_deadline')
            dt_flt1.append('>=')
            prev_day = (datetime.now().date() - relativedelta(days=1)).strftime('%Y/%m/%d')
            dt_flt1.append(prev_day)
            doman.append( tuple(dt_flt1) )
             
            dt_flt2 = []
            dt_flt2.append('date_deadline')
            dt_flt2.append('<=')
            prev_day = (datetime.now().date() - relativedelta(days=1)).strftime('%Y/%m/%d')                                     
            dt_flt2.append(prev_day)
            doman.append( tuple(dt_flt2) ) 
      
        elif crm_days_filter == 'weekly': # current week 
           
            dt_flt1 = []
            dt_flt1.append('date_deadline')
            dt_flt1.append('>')
            dt_flt1.append( (datetime.now().date() - relativedelta(weeks = 1,weekday=0) ).strftime("%Y/%m/%d") )
            doman.append( tuple(dt_flt1) ) 
            
            dt_flt2 = []
            dt_flt2.append('date_deadline')
            dt_flt2.append('<=')
            dt_flt2.append(datetime.now().date().strftime("%Y/%m/%d"))
            doman.append( tuple(dt_flt2) ) 
            
        elif crm_days_filter == 'prev_week': # Previous week 
           
            dt_flt1 = []
            dt_flt1.append('date_deadline')
            dt_flt1.append('>')
            dt_flt1.append( (datetime.now().date() - relativedelta(weeks = 2,weekday=0) ).strftime("%Y/%m/%d") )
            doman.append( tuple(dt_flt1) ) 
            
            dt_flt2 = []
            dt_flt2.append('date_deadline')
            dt_flt2.append('<=')
            dt_flt2.append( (datetime.now().date()- relativedelta(weeks = 1,weekday=6) ).strftime("%Y/%m/%d"))
            doman.append( tuple(dt_flt2) ) 
           
        elif crm_days_filter == 'monthly': # Current Month                     
           
            dt_flt1 = []
            dt_flt1.append('date_deadline')
            dt_flt1.append('>')
            dt_flt1.append( (datetime.now().date() ).strftime("%Y/%m/01") )
            doman.append( tuple(dt_flt1) ) 
            
            dt_flt2 = []
            dt_flt2.append('date_deadline')
            dt_flt2.append('<=')
            dt_flt2.append(datetime.now().date().strftime("%Y/%m/%d"))
            doman.append( tuple(dt_flt2) ) 

        elif crm_days_filter == 'prev_month': # Previous Month                     
           
            dt_flt1 = []
            dt_flt1.append('date_deadline')
            dt_flt1.append('>')
            dt_flt1.append( (datetime.now().date() - relativedelta(months = 1) ).strftime("%Y/%m/01") )
            doman.append( tuple(dt_flt1) ) 
            
            dt_flt2 = []
            dt_flt2.append('date_deadline')
            dt_flt2.append('<')
            dt_flt2.append(datetime.now().date().strftime("%Y/%m/01"))
            doman.append( tuple(dt_flt2) ) 
           
        elif crm_days_filter == 'cur_year': # Current Year                     
           
            dt_flt1 = []
            dt_flt1.append('date_deadline')
            dt_flt1.append('>')
            dt_flt1.append( (datetime.now().date() ).strftime("%Y/01/01") )
            doman.append( tuple(dt_flt1) ) 
            
            dt_flt2 = []
            dt_flt2.append('date_deadline')
            dt_flt2.append('<=')
            dt_flt2.append(datetime.now().date().strftime("%Y/%m/%d"))
            doman.append( tuple(dt_flt2) ) 

        elif crm_days_filter == 'prev_year': # Previous Year                     
           
            dt_flt1 = []
            dt_flt1.append('date_deadline')
            dt_flt1.append('>')
            dt_flt1.append( (datetime.now().date() - relativedelta(years = 1) ).strftime("%Y/01/01") )
            doman.append( tuple(dt_flt1) ) 
            
            dt_flt2 = []
            dt_flt2.append('date_deadline')
            dt_flt2.append('<')
            dt_flt2.append(datetime.now().date().strftime("%Y/01/01"))
            doman.append( tuple(dt_flt2) ) 
           
        elif crm_days_filter == 'custom':
            if  custom_date_start and custom_date_end:
                 
                dt_flt1 = []
                dt_flt1.append('date_deadline')
                dt_flt1.append('>')
                dt_flt1.append( datetime.strptime(str(custom_date_start),DEFAULT_SERVER_DATE_FORMAT).strftime("%Y/%m/%d") )
                doman.append( tuple(dt_flt1) ) 
            
                dt_flt2 = []
                dt_flt2.append('date_deadline')
                dt_flt2.append('<=')
                dt_flt2.append( datetime.strptime(str(custom_date_end),DEFAULT_SERVER_DATE_FORMAT).strftime("%Y/%m/%d"))
                doman.append( tuple(dt_flt2) ) 

#         doman = []
        # FILTER USER
        if filter_user not in ['',"",None,False]:
            doman.append(('user_id','=',int(filter_user)))
        else:
            doman.append(('user_id','=',self.env.user.id))
        if filter_supervisor not in ['',"",None,False]:
            doman.append(('supervisor_id','=',int(filter_supervisor)))
        else:
            doman.append(('supervisor_id','=',self.env.user.id))
        activities = self.env['mail.activity'].search(doman,limit = False, order='res_id desc')
        planned_activities = []
        overdue_activities = []
        all_activities = []
        completed_activities = []
        for activity in activities:
            all_activities.append(activity.id)
            if activity.state in ['planned','today']:
                planned_activities_count+=1
                planned_activities.append(activity.id)
            if activity.state=='overdue':
                overdue_activities_count+=1
                overdue_activities.append(activity.id)
            if activity.state=='done':
                completed_activities_count+=1
                completed_activities.append(activity.id)
        return self.env['ir.ui.view'].with_context().render_template('sh_activities_management.sh_crm_db_activity_count_box', {
            'planned_activities':planned_activities,
            'overdue_activities':overdue_activities,
            'all_activities':all_activities,
            'completed_activities':completed_activities,
            'planned_acitvities_count' : planned_activities_count,
            'overdue_activities_count':overdue_activities_count,
            'completed_activities_count':completed_activities_count,
            'all_activities_count':len(activities.ids),
            })
    
    
    @api.model
    def get_sh_crm_activity_todo_tbl(self,filter_date,filter_user,start_date,end_date,filter_supervisor):
        doman = [('state','in',['planned','today'])]
        crm_days_filter = filter_date 
        custom_date_start = start_date
        custom_date_end = end_date        
        if crm_days_filter == 'today':
           
            dt_flt1 = []
            dt_flt1.append('date_deadline')
            dt_flt1.append('>=')
            dt_flt1.append(datetime.now().date().strftime("%Y/%m/%d"))
            doman.append( tuple(dt_flt1) )
             
            dt_flt2 = []
            dt_flt2.append('date_deadline')
            dt_flt2.append('<=')
            dt_flt2.append(datetime.now().date().strftime("%Y/%m/%d"))
            doman.append( tuple(dt_flt2) )
        elif crm_days_filter == 'yesterday':
           
            dt_flt1 = []
            dt_flt1.append('date_deadline')
            dt_flt1.append('>=')
            prev_day = (datetime.now().date() - relativedelta(days=1)).strftime('%Y/%m/%d')
            dt_flt1.append(prev_day)
            doman.append( tuple(dt_flt1) )
             
            dt_flt2 = []
            dt_flt2.append('date_deadline')
            dt_flt2.append('<=')
            prev_day = (datetime.now().date() - relativedelta(days=1)).strftime('%Y/%m/%d')                                     
            dt_flt2.append(prev_day)
            doman.append( tuple(dt_flt2) ) 
      
        elif crm_days_filter == 'weekly': # current week 
           
            dt_flt1 = []
            dt_flt1.append('date_deadline')
            dt_flt1.append('>')
            dt_flt1.append( (datetime.now().date() - relativedelta(weeks = 1,weekday=0) ).strftime("%Y/%m/%d") )
            doman.append( tuple(dt_flt1) ) 
            
            dt_flt2 = []
            dt_flt2.append('date_deadline')
            dt_flt2.append('<=')
            dt_flt2.append(datetime.now().date().strftime("%Y/%m/%d"))
            doman.append( tuple(dt_flt2) ) 
            
        elif crm_days_filter == 'prev_week': # Previous week 
           
            dt_flt1 = []
            dt_flt1.append('date_deadline')
            dt_flt1.append('>')
            dt_flt1.append( (datetime.now().date() - relativedelta(weeks = 2,weekday=0) ).strftime("%Y/%m/%d") )
            doman.append( tuple(dt_flt1) ) 
            
            dt_flt2 = []
            dt_flt2.append('date_deadline')
            dt_flt2.append('<=')
            dt_flt2.append( (datetime.now().date()- relativedelta(weeks = 1,weekday=6) ).strftime("%Y/%m/%d"))
            doman.append( tuple(dt_flt2) ) 
           
        elif crm_days_filter == 'monthly': # Current Month                     
           
            dt_flt1 = []
            dt_flt1.append('date_deadline')
            dt_flt1.append('>')
            dt_flt1.append( (datetime.now().date() ).strftime("%Y/%m/01") )
            doman.append( tuple(dt_flt1) ) 
            
            dt_flt2 = []
            dt_flt2.append('date_deadline')
            dt_flt2.append('<=')
            dt_flt2.append(datetime.now().date().strftime("%Y/%m/%d"))
            doman.append( tuple(dt_flt2) ) 

        elif crm_days_filter == 'prev_month': # Previous Month                     
           
            dt_flt1 = []
            dt_flt1.append('date_deadline')
            dt_flt1.append('>')
            dt_flt1.append( (datetime.now().date() - relativedelta(months = 1) ).strftime("%Y/%m/01") )
            doman.append( tuple(dt_flt1) ) 
            
            dt_flt2 = []
            dt_flt2.append('date_deadline')
            dt_flt2.append('<')
            dt_flt2.append(datetime.now().date().strftime("%Y/%m/01"))
            doman.append( tuple(dt_flt2) ) 
           
        elif crm_days_filter == 'cur_year': # Current Year                     
           
            dt_flt1 = []
            dt_flt1.append('date_deadline')
            dt_flt1.append('>')
            dt_flt1.append( (datetime.now().date() ).strftime("%Y/01/01") )
            doman.append( tuple(dt_flt1) ) 
            
            dt_flt2 = []
            dt_flt2.append('date_deadline')
            dt_flt2.append('<=')
            dt_flt2.append(datetime.now().date().strftime("%Y/%m/%d"))
            doman.append( tuple(dt_flt2) ) 

        elif crm_days_filter == 'prev_year': # Previous Year                     
           
            dt_flt1 = []
            dt_flt1.append('date_deadline')
            dt_flt1.append('>')
            dt_flt1.append( (datetime.now().date() - relativedelta(years = 1) ).strftime("%Y/01/01") )
            doman.append( tuple(dt_flt1) ) 
            
            dt_flt2 = []
            dt_flt2.append('date_deadline')
            dt_flt2.append('<')
            dt_flt2.append(datetime.now().date().strftime("%Y/01/01"))
            doman.append( tuple(dt_flt2) ) 
           
        elif crm_days_filter == 'custom':
            if  custom_date_start and custom_date_end:
                 
                dt_flt1 = []
                dt_flt1.append('date_deadline')
                dt_flt1.append('>')
                dt_flt1.append( datetime.strptime(str(custom_date_start),DEFAULT_SERVER_DATE_FORMAT).strftime("%Y/%m/%d") )
                doman.append( tuple(dt_flt1) ) 
            
                dt_flt2 = []
                dt_flt2.append('date_deadline')
                dt_flt2.append('<=')
                dt_flt2.append( datetime.strptime(str(custom_date_end),DEFAULT_SERVER_DATE_FORMAT).strftime("%Y/%m/%d"))
                doman.append( tuple(dt_flt2) ) 

#         doman = []
        # FILTER USER
        if filter_user not in ['',"",None,False]:
            doman.append(('user_id','=',int(filter_user)))
        else:
            doman.append(('user_id','=',self.env.user.id))
        if filter_supervisor not in ['',"",None,False]:
            doman.append(('supervisor_id','=',int(filter_supervisor)))
        else:
            doman.append(('supervisor_id','=',self.env.user.id))
        activities = self.env['mail.activity'].sudo().search(doman,limit = False, order='res_id desc')
        return self.env['ir.ui.view'].with_context().render_template('sh_activities_management.sh_crm_db_activity_todo_tbl', {
            'activities': activities,
            'planned_acitvities_count' : len(activities.ids),
            })
    
    
    @api.model
    def get_sh_crm_activity_all_tbl(self,filter_date,filter_user,start_date,end_date,filter_supervisor):
        doman = []

        crm_days_filter = filter_date 
        custom_date_start = start_date
        custom_date_end = end_date         
        if crm_days_filter == 'today':
           
            dt_flt1 = []
            dt_flt1.append('date_deadline')
            dt_flt1.append('>=')
            dt_flt1.append(datetime.now().date().strftime("%Y/%m/%d"))
            doman.append( tuple(dt_flt1) )
             
            dt_flt2 = []
            dt_flt2.append('date_deadline')
            dt_flt2.append('<=')
            dt_flt2.append(datetime.now().date().strftime("%Y/%m/%d"))
            doman.append( tuple(dt_flt2) )
        elif crm_days_filter == 'yesterday':
           
            dt_flt1 = []
            dt_flt1.append('date_deadline')
            dt_flt1.append('>=')
            prev_day = (datetime.now().date() - relativedelta(days=1)).strftime('%Y/%m/%d')
            dt_flt1.append(prev_day)
            doman.append( tuple(dt_flt1) )
             
            dt_flt2 = []
            dt_flt2.append('date_deadline')
            dt_flt2.append('<=')
            prev_day = (datetime.now().date() - relativedelta(days=1)).strftime('%Y/%m/%d')                                     
            dt_flt2.append(prev_day)
            doman.append( tuple(dt_flt2) ) 
      
        elif crm_days_filter == 'weekly': # current week 
           
            dt_flt1 = []
            dt_flt1.append('date_deadline')
            dt_flt1.append('>')
            dt_flt1.append( (datetime.now().date() - relativedelta(weeks = 1,weekday=0) ).strftime("%Y/%m/%d") )
            doman.append( tuple(dt_flt1) ) 
            
            dt_flt2 = []
            dt_flt2.append('date_deadline')
            dt_flt2.append('<=')
            dt_flt2.append(datetime.now().date().strftime("%Y/%m/%d"))
            doman.append( tuple(dt_flt2) ) 
            
            
        elif crm_days_filter == 'prev_week': # Previous week 
           
            dt_flt1 = []
            dt_flt1.append('date_deadline')
            dt_flt1.append('>')
            dt_flt1.append( (datetime.now().date() - relativedelta(weeks = 2,weekday=0) ).strftime("%Y/%m/%d") )
            doman.append( tuple(dt_flt1) ) 
            
            dt_flt2 = []
            dt_flt2.append('date_deadline')
            dt_flt2.append('<=')
            dt_flt2.append( (datetime.now().date()- relativedelta(weeks = 1,weekday=6) ).strftime("%Y/%m/%d"))
            doman.append( tuple(dt_flt2) ) 
           
        elif crm_days_filter == 'monthly': # Current Month                     
           
            dt_flt1 = []
            dt_flt1.append('date_deadline')
            dt_flt1.append('>')
            dt_flt1.append( (datetime.now().date() ).strftime("%Y/%m/01") )
            doman.append( tuple(dt_flt1) ) 
            
            dt_flt2 = []
            dt_flt2.append('date_deadline')
            dt_flt2.append('<=')
            dt_flt2.append(datetime.now().date().strftime("%Y/%m/%d"))
            doman.append( tuple(dt_flt2) ) 

        elif crm_days_filter == 'prev_month': # Previous Month                     
           
            dt_flt1 = []
            dt_flt1.append('date_deadline')
            dt_flt1.append('>')
            dt_flt1.append( (datetime.now().date() - relativedelta(months = 1) ).strftime("%Y/%m/01") )
            doman.append( tuple(dt_flt1) ) 
            
            dt_flt2 = []
            dt_flt2.append('date_deadline')
            dt_flt2.append('<')
            dt_flt2.append(datetime.now().date().strftime("%Y/%m/01"))
            doman.append( tuple(dt_flt2) ) 
           
        elif crm_days_filter == 'cur_year': # Current Year                     
           
            dt_flt1 = []
            dt_flt1.append('date_deadline')
            dt_flt1.append('>')
            dt_flt1.append( (datetime.now().date() ).strftime("%Y/01/01") )
            doman.append( tuple(dt_flt1) ) 
            
            dt_flt2 = []
            dt_flt2.append('date_deadline')
            dt_flt2.append('<=')
            dt_flt2.append(datetime.now().date().strftime("%Y/%m/%d"))
            doman.append( tuple(dt_flt2) ) 

        elif crm_days_filter == 'prev_year': # Previous Year                     
           
            dt_flt1 = []
            dt_flt1.append('date_deadline')
            dt_flt1.append('>')
            dt_flt1.append( (datetime.now().date() - relativedelta(years = 1) ).strftime("%Y/01/01") )
            doman.append( tuple(dt_flt1) ) 
            
            dt_flt2 = []
            dt_flt2.append('date_deadline')
            dt_flt2.append('<')
            dt_flt2.append(datetime.now().date().strftime("%Y/01/01"))
            doman.append( tuple(dt_flt2) ) 
           
        elif crm_days_filter == 'custom':
            if  custom_date_start and custom_date_end:
                 
                dt_flt1 = []
                dt_flt1.append('date_deadline')
                dt_flt1.append('>')
                dt_flt1.append( datetime.strptime(str(custom_date_start),DEFAULT_SERVER_DATE_FORMAT).strftime("%Y/%m/%d") )
                doman.append( tuple(dt_flt1) ) 
            
                dt_flt2 = []
                dt_flt2.append('date_deadline')
                dt_flt2.append('<=')
                dt_flt2.append( datetime.strptime(str(custom_date_end),DEFAULT_SERVER_DATE_FORMAT).strftime("%Y/%m/%d"))
                doman.append( tuple(dt_flt2) ) 

#         doman = []
        # FILTER USER
        if filter_user not in ['',"",None,False]:
            doman.append(('user_id','=',int(filter_user)))
        else:
            doman.append(('user_id','=',self.env.user.id))
        if filter_supervisor not in ['',"",None,False]:
            doman.append(('supervisor_id','=',int(filter_supervisor)))
        else:
            doman.append(('supervisor_id','=',self.env.user.id))
        activities = self.env['mail.activity'].sudo().search(doman,limit = False, order='res_id desc')
        
        return self.env['ir.ui.view'].with_context().render_template('sh_activities_management.sh_crm_db_activity_all_tbl', {
            'activities': activities,
            'all_acitvities_count' : len(activities.ids),
            })
    
    @api.model
    def get_sh_crm_activity_completed_tbl(self,filter_date,filter_user,start_date,end_date,filter_supervisor):
        doman = [('state','in',['done'])]

        crm_days_filter = filter_date 
        custom_date_start = start_date
        custom_date_end = end_date         
        if crm_days_filter == 'today':
           
            dt_flt1 = []
            dt_flt1.append('date_deadline')
            dt_flt1.append('>=')
            dt_flt1.append(datetime.now().date().strftime("%Y/%m/%d"))
            doman.append( tuple(dt_flt1) )
             
            dt_flt2 = []
            dt_flt2.append('date_deadline')
            dt_flt2.append('<=')
            dt_flt2.append(datetime.now().date().strftime("%Y/%m/%d"))
            doman.append( tuple(dt_flt2) )
        elif crm_days_filter == 'yesterday':
           
            dt_flt1 = []
            dt_flt1.append('date_deadline')
            dt_flt1.append('>=')
            prev_day = (datetime.now().date() - relativedelta(days=1)).strftime('%Y/%m/%d')
            dt_flt1.append(prev_day)
            doman.append( tuple(dt_flt1) )
             
            dt_flt2 = []
            dt_flt2.append('date_deadline')
            dt_flt2.append('<=')
            prev_day = (datetime.now().date() - relativedelta(days=1)).strftime('%Y/%m/%d')                                     
            dt_flt2.append(prev_day)
            doman.append( tuple(dt_flt2) ) 
      
        elif crm_days_filter == 'weekly': # current week 
           
            dt_flt1 = []
            dt_flt1.append('date_deadline')
            dt_flt1.append('>')
            dt_flt1.append( (datetime.now().date() - relativedelta(weeks = 1,weekday=0) ).strftime("%Y/%m/%d") )
            doman.append( tuple(dt_flt1) ) 
            
            dt_flt2 = []
            dt_flt2.append('date_deadline')
            dt_flt2.append('<=')
            dt_flt2.append(datetime.now().date().strftime("%Y/%m/%d"))
            doman.append( tuple(dt_flt2) ) 
            
        elif crm_days_filter == 'prev_week': # Previous week 
           
            dt_flt1 = []
            dt_flt1.append('date_deadline')
            dt_flt1.append('>')
            dt_flt1.append( (datetime.now().date() - relativedelta(weeks = 2,weekday=0) ).strftime("%Y/%m/%d") )
            doman.append( tuple(dt_flt1) ) 
            
            dt_flt2 = []
            dt_flt2.append('date_deadline')
            dt_flt2.append('<=')
            dt_flt2.append( (datetime.now().date()- relativedelta(weeks = 1,weekday=6) ).strftime("%Y/%m/%d"))
            doman.append( tuple(dt_flt2) ) 
           
        elif crm_days_filter == 'monthly': # Current Month                     
           
            dt_flt1 = []
            dt_flt1.append('date_deadline')
            dt_flt1.append('>')
            dt_flt1.append( (datetime.now().date() ).strftime("%Y/%m/01") )
            doman.append( tuple(dt_flt1) ) 
            
            dt_flt2 = []
            dt_flt2.append('date_deadline')
            dt_flt2.append('<=')
            dt_flt2.append(datetime.now().date().strftime("%Y/%m/%d"))
            doman.append( tuple(dt_flt2) ) 

        elif crm_days_filter == 'prev_month': # Previous Month                     
           
            dt_flt1 = []
            dt_flt1.append('date_deadline')
            dt_flt1.append('>')
            dt_flt1.append( (datetime.now().date() - relativedelta(months = 1) ).strftime("%Y/%m/01") )
            doman.append( tuple(dt_flt1) ) 
            
            dt_flt2 = []
            dt_flt2.append('date_deadline')
            dt_flt2.append('<')
            dt_flt2.append(datetime.now().date().strftime("%Y/%m/01"))
            doman.append( tuple(dt_flt2) ) 
           
        elif crm_days_filter == 'cur_year': # Current Year                     
           
            dt_flt1 = []
            dt_flt1.append('date_deadline')
            dt_flt1.append('>')
            dt_flt1.append( (datetime.now().date() ).strftime("%Y/01/01") )
            doman.append( tuple(dt_flt1) ) 
            
            dt_flt2 = []
            dt_flt2.append('date_deadline')
            dt_flt2.append('<=')
            dt_flt2.append(datetime.now().date().strftime("%Y/%m/%d"))
            doman.append( tuple(dt_flt2) ) 

        elif crm_days_filter == 'prev_year': # Previous Year                     
           
            dt_flt1 = []
            dt_flt1.append('date_deadline')
            dt_flt1.append('>')
            dt_flt1.append( (datetime.now().date() - relativedelta(years = 1) ).strftime("%Y/01/01") )
            doman.append( tuple(dt_flt1) ) 
            
            dt_flt2 = []
            dt_flt2.append('date_deadline')
            dt_flt2.append('<')
            dt_flt2.append(datetime.now().date().strftime("%Y/01/01"))
            doman.append( tuple(dt_flt2) ) 
           
        elif crm_days_filter == 'custom':
            if  custom_date_start and custom_date_end:
                 
                dt_flt1 = []
                dt_flt1.append('date_deadline')
                dt_flt1.append('>')
                dt_flt1.append( datetime.strptime(str(custom_date_start),DEFAULT_SERVER_DATE_FORMAT).strftime("%Y/%m/%d") )
                doman.append( tuple(dt_flt1) ) 
            
                dt_flt2 = []
                dt_flt2.append('date_deadline')
                dt_flt2.append('<=')
                dt_flt2.append( datetime.strptime(str(custom_date_end),DEFAULT_SERVER_DATE_FORMAT).strftime("%Y/%m/%d"))
                doman.append( tuple(dt_flt2) ) 

#         doman = []
        # FILTER USER
        if filter_user not in ['',"",None,False]:
            doman.append(('user_id','=',int(filter_user)))
        else:
            doman.append(('user_id','=',self.env.user.id))
        if filter_supervisor not in ['',"",None,False]:
            doman.append(('supervisor_id','=',int(filter_supervisor)))
        else:
            doman.append(('supervisor_id','=',self.env.user.id))
        activities = self.env['mail.activity'].sudo().search(doman,limit = False, order='res_id desc')
        
        return self.env['ir.ui.view'].with_context().render_template('sh_activities_management.sh_crm_db_activity_completed_tbl', {
            'activities': activities,
            'completed_acitvities_count' : len(activities.ids),
            })
        
    @api.model
    def get_sh_crm_activity_overdue_tbl(self,filter_date,filter_user,start_date,end_date,filter_supervisor):
        doman = [('state','in',['overdue'])]

        crm_days_filter = filter_date 
        custom_date_start = start_date
        custom_date_end = end_date         
        if crm_days_filter == 'today':
           
            dt_flt1 = []
            dt_flt1.append('date_deadline')
            dt_flt1.append('>=')
            dt_flt1.append(datetime.now().date().strftime("%Y/%m/%d"))
            doman.append( tuple(dt_flt1) )
             
            dt_flt2 = []
            dt_flt2.append('date_deadline')
            dt_flt2.append('<=')
            dt_flt2.append(datetime.now().date().strftime("%Y/%m/%d"))
            doman.append( tuple(dt_flt2) )
        elif crm_days_filter == 'yesterday':
           
            dt_flt1 = []
            dt_flt1.append('date_deadline')
            dt_flt1.append('>=')
            prev_day = (datetime.now().date() - relativedelta(days=1)).strftime('%Y/%m/%d')
            dt_flt1.append(prev_day)
            doman.append( tuple(dt_flt1) )
             
            dt_flt2 = []
            dt_flt2.append('date_deadline')
            dt_flt2.append('<=')
            prev_day = (datetime.now().date() - relativedelta(days=1)).strftime('%Y/%m/%d')                                     
            dt_flt2.append(prev_day)
            doman.append( tuple(dt_flt2) ) 
      
        elif crm_days_filter == 'weekly': # current week 
           
            dt_flt1 = []
            dt_flt1.append('date_deadline')
            dt_flt1.append('>')
            dt_flt1.append( (datetime.now().date() - relativedelta(weeks = 1,weekday=0) ).strftime("%Y/%m/%d") )
            doman.append( tuple(dt_flt1) ) 
            
            dt_flt2 = []
            dt_flt2.append('date_deadline')
            dt_flt2.append('<=')
            dt_flt2.append(datetime.now().date().strftime("%Y/%m/%d"))
            doman.append( tuple(dt_flt2) ) 
            
        elif crm_days_filter == 'prev_week': # Previous week 
           
            dt_flt1 = []
            dt_flt1.append('date_deadline')
            dt_flt1.append('>')
            dt_flt1.append( (datetime.now().date() - relativedelta(weeks = 2,weekday=0) ).strftime("%Y/%m/%d") )
            doman.append( tuple(dt_flt1) ) 
            
            dt_flt2 = []
            dt_flt2.append('date_deadline')
            dt_flt2.append('<=')
            dt_flt2.append( (datetime.now().date()- relativedelta(weeks = 1,weekday=6) ).strftime("%Y/%m/%d"))
            doman.append( tuple(dt_flt2) ) 
           
        elif crm_days_filter == 'monthly': # Current Month                     
           
            dt_flt1 = []
            dt_flt1.append('date_deadline')
            dt_flt1.append('>')
            dt_flt1.append( (datetime.now().date() ).strftime("%Y/%m/01") )
            doman.append( tuple(dt_flt1) ) 
            
            dt_flt2 = []
            dt_flt2.append('date_deadline')
            dt_flt2.append('<=')
            dt_flt2.append(datetime.now().date().strftime("%Y/%m/%d"))
            doman.append( tuple(dt_flt2) ) 

        elif crm_days_filter == 'prev_month': # Previous Month                     
           
            dt_flt1 = []
            dt_flt1.append('date_deadline')
            dt_flt1.append('>')
            dt_flt1.append( (datetime.now().date() - relativedelta(months = 1) ).strftime("%Y/%m/01") )
            doman.append( tuple(dt_flt1) ) 
            
            dt_flt2 = []
            dt_flt2.append('date_deadline')
            dt_flt2.append('<')
            dt_flt2.append(datetime.now().date().strftime("%Y/%m/01"))
            doman.append( tuple(dt_flt2) ) 
           
        elif crm_days_filter == 'cur_year': # Current Year                     
           
            dt_flt1 = []
            dt_flt1.append('date_deadline')
            dt_flt1.append('>')
            dt_flt1.append( (datetime.now().date() ).strftime("%Y/01/01") )
            doman.append( tuple(dt_flt1) ) 
            
            dt_flt2 = []
            dt_flt2.append('date_deadline')
            dt_flt2.append('<=')
            dt_flt2.append(datetime.now().date().strftime("%Y/%m/%d"))
            doman.append( tuple(dt_flt2) ) 

        elif crm_days_filter == 'prev_year': # Previous Year                     
           
            dt_flt1 = []
            dt_flt1.append('date_deadline')
            dt_flt1.append('>')
            dt_flt1.append( (datetime.now().date() - relativedelta(years = 1) ).strftime("%Y/01/01") )
            doman.append( tuple(dt_flt1) ) 
            
            dt_flt2 = []
            dt_flt2.append('date_deadline')
            dt_flt2.append('<')
            dt_flt2.append(datetime.now().date().strftime("%Y/01/01"))
            doman.append( tuple(dt_flt2) ) 
           
        elif crm_days_filter == 'custom':
            if  custom_date_start and custom_date_end:
                 
                dt_flt1 = []
                dt_flt1.append('date_deadline')
                dt_flt1.append('>')
                dt_flt1.append( datetime.strptime(str(custom_date_start),DEFAULT_SERVER_DATE_FORMAT).strftime("%Y/%m/%d") )
                doman.append( tuple(dt_flt1) ) 
            
                dt_flt2 = []
                dt_flt2.append('date_deadline')
                dt_flt2.append('<=')
                dt_flt2.append( datetime.strptime(str(custom_date_end),DEFAULT_SERVER_DATE_FORMAT).strftime("%Y/%m/%d"))
                doman.append( tuple(dt_flt2) ) 

#         doman = []
        # FILTER USER
        if filter_user not in ['',"",None,False]:
            doman.append(('user_id','=',int(filter_user)))
        else:
            doman.append(('user_id','=',self.env.user.id))
        if filter_supervisor not in ['',"",None,False]:
            doman.append(('supervisor_id','=',int(filter_supervisor)))
        else:
            doman.append(('supervisor_id','=',self.env.user.id))
        activities = self.env['mail.activity'].sudo().search(doman,limit = False, order='res_id desc')
        
        return self.env['ir.ui.view'].with_context().render_template('sh_activities_management.sh_crm_db_activity_overdue_tbl', {
            'activities': activities,
            'overdue_acitvities_count' : len(activities.ids),
            })


    @api.model
    def get_user_list(self):                             
        domain = []
                                
        users = self.env["res.users"].sudo().search_read(domain)
                           
        return users   



