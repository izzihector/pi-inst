odoo.define('pivotino_feedback_dashboard.DashboardController', function (require) {
    "use strict";

    var config = require('web.config');

    if (config.device.isMobile) {
        return;
    }

    var KsDashboardNinja = require('ks_dashboard_ninja.ks_dashboard');
    var FeedbackSnackbar = require('pivotino_feedback.feedback_snackbar');
    var session = require('web.session');

    KsDashboardNinja.include({
        // rendering dashboard
        ksRenderDashboard: function() {
            var self = this;
            var proms = [];
            this._super.apply(this, arguments);

            this._rpc({
                model: 'res.users',
                method: 'check_dashboard_feedback',
                args: [[session.uid]],
            }).then(function (val) {
                if (val['lost']) {
                    var option = "Missed Sales";
                    var value = "Does Pivotino help you focus better on missed opportunities and drill down to the reasons of lost?";
                    self.feedback_wizard = new FeedbackSnackbar(self, option, value);
                    var $action_manager = document.querySelector('.o_action_manager');
                    proms.push(self.feedback_wizard.insertAfter($action_manager));
                    return Promise.all(proms);
                } else if (val['won']) {
                    var option = "Actual Sales";
                    var value = "Are you satisfied on how Pivotino gives you a quick analysis of your actual sales vs your target?";
                    self.feedback_wizard = new FeedbackSnackbar(self, option, value);
                    var $action_manager = document.querySelector('.o_action_manager');
                    proms.push(self.feedback_wizard.insertAfter($action_manager));
                    return Promise.all(proms);
                } else {
                    return;
                }
            });
        },
    });
});