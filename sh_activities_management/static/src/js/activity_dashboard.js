odoo.define('sh_activities_management.dashboard', function(require) {
    "use strict";
    
    var AbstractAction = require('web.AbstractAction');
	var ajax = require('web.ajax');
	var core = require('web.core');
	var rpc = require('web.rpc');
	var session = require('web.session');
	var web_client = require('web.web_client');
	var _t = core._t;
	var QWeb = core.qweb;
    
    

    var ActivityDashboardView = AbstractAction.extend({
        events: {
            'click .card_1': 'action_all_activities',
            'click .card_2': 'action_planned_activities',
            'click .card_4': 'action_overdue_activities',
            'click .card_3': 'action_completed_activities',
            'click  .mark-done': 'action_done',
            'click .mark-view': 'action_view',
            'change  #crm_days_filter_list': 'render_activity_tbl',            
            'change  #sh_crm_db_user_id': 'render_activity_tbl',
            'change  #sh_crm_db_supervisor_id': 'render_activity_tbl',
            'change  #start_date': 'render_activity_tbl',
            'change  #end_date': 'render_activity_tbl',    
        },
        init: function(parent, context) {
            this._super(parent, context);
            var crm_data = [];
            var res = ''
            var self = this;
            if (context.tag == 'activity_dashboard.dashboard') {
      
					this._rpc({
                    	model: 'activity.dashboard',
                        method: 'get_user_list',
                    })
                    .then(function (messagesData) {
                    self.render();
               	$('#sh_crm_db_user_id > option').remove();
               	$('#sh_crm_db_supervisor_id > option').remove();
               	session.user_has_group('sh_activities_management.group_activity_supervisor')
                .then(function (has_group) {
                    if (has_group) {
                    	$('#sh_crm_db_supervisor_id').removeClass("o_hidden");
                    }
                });
               	session.user_has_group('sh_activities_management.group_activity_manager')
                .then(function (has_group) {
                    if (has_group) {
                        $('#sh_crm_db_supervisor_id').removeClass("o_hidden");
                        $('#sh_crm_db_user_id').removeClass("o_hidden");
                    }
                });
				$('#sh_crm_db_user_id').append(
						  '<option value="">Users</option>'
			          );                    
                $('#sh_crm_db_supervisor_id').append(
						  '<option value="">Supervisors</option>'
			          ); 
                        _.each(messagesData, function (data) {
				            	$('#sh_crm_db_user_id').append(
				      					  '<option value="' + data.id + '">' + data.name + '</option>'
				                        );		
				               	$('#sh_crm_db_supervisor_id').append(
				      					  '<option value="' + data.id + '">' + data.name + '</option>'
				                        );	
				               	self.render_activity_tbl();
                        });
                    });             				
				

//self.render_activity_tbl();


            
            }            
            
            
        },



        willStart: function() {
            return $.when(ajax.loadLibs(this), this._super());
            
        },
        start: function() {
            var self = this;
            return this._super();
        },

        render: function() {
            var self = this;
            var crm_dashboard = QWeb.render('activity_dashboard.dashboard', {
                widget: self,
            });
            //$(".o_control_panel").addClass("o_hidden");
            $(crm_dashboard).prependTo(self.$el);
            return crm_dashboard
        },
        reload: function() {
            location.reload();

        },
        
        action_all_activities: function(event) {
            var self = this;
            var all_act = [];
    		$('#all_activity:checked').each(function() {
    		var total = $(this).attr('value');
    		all_act.push(total);
  			});
  			event.stopPropagation();
            event.preventDefault();
            self.do_action({
                name: _t("All Activities"),
                type: 'ir.actions.act_window',
                res_model: 'mail.activity',
                view_mode: 'tree,form',
                view_type: 'form',
                views: [
                    [false, 'list'],
                    [false, 'form']
                ],
                domain: [
                    ['id', 'in', all_act],
                ],
                target: 'current'
            }, {

            })
        },
		
		action_completed_activities: function(event) {
            var self = this;
            var all_act = [];
    		$('#completed_activity:checked').each(function() {
    		var total = $(this).attr('value');
    		all_act.push(total);
  			});
  			event.stopPropagation();
            event.preventDefault();
            self.do_action({
                name: _t("Completed Activities"),
                type: 'ir.actions.act_window',
                res_model: 'mail.activity',
                view_mode: 'tree,form',
                view_type: 'form',
                views: [
                    [false, 'list'],
                    [false, 'form']
                ],
                domain: [
                    ['id', 'in', all_act],
                ],
                target: 'current'
            }, {

            })
        },
		
		
		action_planned_activities: function(event) {
            var self = this;
            var all_act = [];
    		$('#planned_activity:checked').each(function() {
    		var total = $(this).attr('value');
    		all_act.push(total);
  			});
  			event.stopPropagation();
            event.preventDefault();
            self.do_action({
                name: _t("Planned Activities"),
                type: 'ir.actions.act_window',
                res_model: 'mail.activity',
                view_mode: 'tree,form',
                view_type: 'form',
                views: [
                    [false, 'list'],
                    [false, 'form']
                ],
                domain: [
                    ['id', 'in', all_act],
                ],
                target: 'current'
            }, {

            })
        },
		
		action_overdue_activities: function(event) {
            var self = this;
            var all_act = [];
    		$('#overdue_activity:checked').each(function() {
    		var total = $(this).attr('value');
    		all_act.push(total);
  			});
  			event.stopPropagation();
            event.preventDefault();
            self.do_action({
                name: _t("Overdue Activities"),
                type: 'ir.actions.act_window',
                res_model: 'mail.activity',
                view_mode: 'tree,form',
                view_type: 'form',
                views: [
                    [false, 'list'],
                    [false, 'form']
                ],
                domain: [
                    ['id', 'in', all_act],
                ],
                target: 'current'
            }, {

            })
        },

        render_activity_tbl: function(event) {


            var self = this;
            
		/*var days_filter= $('#crm_days_filter_list').val();
            
		
		/*
		 * ================================================
		 * CRM ACTIVITY TODO
		 * ================================================
		 */
		 
					 
			var filter_date = $('#crm_days_filter_list').children("option:selected").val();
			var filter_user = $('#sh_crm_db_user_id').children("option:selected").val();
			var filter_supervisor = $('#sh_crm_db_supervisor_id').children("option:selected").val();
			var start_date = $('#start_date').val();
			var end_date = $('#end_date').val();
			
			if (filter_date == 'custom')
		{
		 	$('#start_date_div').css("display", "block");
		 	$('#end_date_div').css("display", "block");
		}
		else
		{
		 	$('#start_date_div').css("display", "none");
		 	$('#end_date_div').css("display", "none");
		 	$('#start_date').val('');
		 	$('#end_date').val('');
		}    
			//Planned Activity
					this._rpc({
                    	model: 'activity.dashboard',
                        method: 'get_sh_crm_activity_todo_tbl',
     					args: [filter_date, filter_user,start_date,end_date,filter_supervisor],                        
                        
                    })
                    .then(function (messagesData) {
					$("#js_id_sh_crm_activity_todo_tbl_div").replaceWith( messagesData );
                        				
                    });             				
				
			//All Activity
					this._rpc({
                    	model: 'activity.dashboard',
                        method: 'get_sh_crm_activity_all_tbl',
     					args: [filter_date, filter_user,start_date,end_date,filter_supervisor],                        
                        
                    })
                    .then(function (messagesData) {
					$("#js_id_sh_crm_activity_all_tbl_div").replaceWith( messagesData );
                        				
                    });
                    
                    
            //Completed Activity
					this._rpc({
                    	model: 'activity.dashboard',
                        method: 'get_sh_crm_activity_completed_tbl',
     					args: [filter_date, filter_user,start_date,end_date,filter_supervisor],                        
                        
                    })
                    .then(function (messagesData) {
					$("#js_id_sh_crm_activity_completed_tbl_div").replaceWith( messagesData );
                        				
                    });
                    
            //Overdue Activity
					this._rpc({
                    	model: 'activity.dashboard',
                        method: 'get_sh_crm_activity_overdue_tbl',
     					args: [filter_date, filter_user,start_date,end_date,filter_supervisor],                        
                        
                    })
                    .then(function (messagesData) {
					$("#js_id_sh_crm_activity_overdue_tbl_div").replaceWith( messagesData );
                        				
                    });
            //activity counts
				this._rpc({
                    	model: 'activity.dashboard',
                        method: 'get_sh_crm_activity_planned_count_tbl',
     					args: [filter_date, filter_user,start_date,end_date,filter_supervisor],                        
                        
                    })
                    .then(function (messagesData) {
					$("#js_id_sh_crm_activity_all_count_tbl_div").replaceWith( messagesData );
                        				
                    });
				
						
		

		
		
		/*
		 * ================================================
		 * CRM CRM ACTIVITY TODO
		 * ================================================
		 */	
		             
            
        },



        action_done: function(e) {
            var self = this;
            var today = new moment().utc().format();
            event.stopPropagation();
            event.preventDefault();
            var $el = $(e.target).parents('tr').find("#h_v").attr("value")
            var activity_id = parseInt($el)
            this._rpc({
                model: 'mail.activity',
                method: 'action_done',
                args: [activity_id],
            }).then(function() {
                self.reload();
            });
        },
        
        
        action_view: function(e) {
            var self = this;
            var today = new moment().utc().format();
            event.stopPropagation();
            event.preventDefault();
            var $el = $(e.target).parents('tr').find("#h_v").attr("value")
            var activity_id = parseInt($el)
            self.do_action({
                name: _t("Activity"),
                type: 'ir.actions.act_window',
                res_model: 'mail.activity',
                view_mode: 'tree,form',
                view_type: 'form',
                views: [
                    [false, 'list'],
                    [false, 'form']
                ],
                domain: [
                    ['id', '=',activity_id ],
                ],
                target: 'current'
            }, {

            })
        },

    });
    core.action_registry.add('activity_dashboard.dashboard', ActivityDashboardView);
    return ActivityDashboardView

});