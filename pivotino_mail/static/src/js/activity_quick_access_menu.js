odoo.define('pivotino_mail.activity_quick_access_menu', function(require){
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var ajax = require('web.ajax');
    var core = require('web.core');
    var rpc = require('web.rpc');
    var session = require('web.session');
    var web_client = require('web.web_client');
    var _t = core._t;
    var QWeb = core.qweb;
    var uid = session.uid;

    var ActivityQuickAccessMenuView = AbstractAction.extend({
        events: {
            'click .card_action_all_activity': 'action_all_activity',
            'click .card_action_future_due_activity': 'action_future_due_activity',
            'click .card_action_today_activity': 'action_today_activity',
            'click .card_action_overdue_activity': 'action_overdue_activity',
        },
        init: function(parent, context) {
            this._super(parent, context);
            var self = this;
            this.action_tag = context.tag;
        },
        willStart: function() {
            return $.when(ajax.loadLibs(this), this._super());

        },
        start: function() {
            var self = this;
            if (this.action_tag == 'pivotino_mail.activity_quick_access_menu'){
                self.render();
                self.render_activity_summary();
            }
            return this._super();
        },
        render: function() {
            var self = this;
            var activity_quick_access_menu = QWeb.render(
            'pivotino_mail.activity_quick_access_menu', {
                widget: self,
            });
            $(activity_quick_access_menu).prependTo(self.$el);
            return activity_quick_access_menu
        },
        render_activity_summary: function(event) {
            var self = this;
            self._rpc({
                model: 'res.users',
                method: 'get_activity_summary',
                args: [uid],
            }).then(function (summary){
                $('#pivotino_activity_cards').replaceWith(summary);
            });
        },
        action_all_activity: function(event){
            var self = this;
            event.stopPropagation();
            event.preventDefault();

            self._rpc({
                model: 'res.users',
                method: 'get_all_activity',
                args: [uid],
            }).then(function (activities){
                self.do_action({
                    name: _t("All Activities"),
                    type: 'ir.actions.act_window',
                    res_model: 'mail.activity',
                    view_mode: 'tree,form',
                    view_type: 'form',
                    views: [
                        [false, 'kanban'],
                        [false, 'list'],
                    ],
                    domain: [
                        ['id', 'in', activities],
                    ],
                    target: 'current',
                    context: {
                        'search_default_my_activities': 1,
                    }
                })
            });
        },
        action_future_due_activity: function(event){
            var self = this;
            event.stopPropagation();
            event.preventDefault();

            self._rpc({
                model: 'res.users',
                method: 'get_future_due_activity',
                args: [uid],
            }).then(function (activities){
                self.do_action({
                    name: _t("Future Due Activities"),
                    type: 'ir.actions.act_window',
                    res_model: 'mail.activity',
                    view_mode: 'tree,form',
                    view_type: 'form',
                    views: [
                        [false, 'kanban'],
                        [false, 'list'],
                    ],
                    domain: [
                        ['id', 'in', activities],
                    ],
                    target: 'current',
                    context: {
                        'search_default_my_activities': 1,
                    }
                })
            });
        },
        action_today_activity: function(event){
            var self = this;
            event.stopPropagation();
            event.preventDefault();

            self._rpc({
                model: 'res.users',
                method: 'get_today_activity',
                args: [uid],
            }).then(function (activities){
                self.do_action({
                    name: _t("Today Activities"),
                    type: 'ir.actions.act_window',
                    res_model: 'mail.activity',
                    view_mode: 'tree,form',
                    view_type: 'form',
                    views: [
                        [false, 'kanban'],
                        [false, 'list'],
                    ],
                    domain: [
                        ['id', 'in', activities],
                    ],
                    target: 'current',
                    context: {
                        'search_default_my_activities': 1,
                    }
                })
            });
        },
        action_overdue_activity: function(event){
            var self = this;
            event.stopPropagation();
            event.preventDefault();

            self._rpc({
                model: 'res.users',
                method: 'get_overdue_activity',
                args: [uid],
            }).then(function (activities){
                self.do_action({
                    name: _t("Overdue Activities"),
                    type: 'ir.actions.act_window',
                    res_model: 'mail.activity',
                    view_mode: 'tree,form',
                    view_type: 'form',
                    views: [
                        [false, 'kanban'],
                        [false, 'list'],
                    ],
                    domain: [
                        ['id', 'in', activities],
                    ],
                    target: 'current',
                    context: {
                        'search_default_my_activities': 1,
                    }
                })
            });
        },
    });
    core.action_registry.add('pivotino_mail.activity_quick_access_menu', ActivityQuickAccessMenuView);
    return ActivityQuickAccessMenuView

});