odoo.define('pivotino_feedback_calendar.CalendarController', function (require) {
    "use strict";

    var config = require('web.config');

    if (config.device.isMobile) {
        return;
    }

    var CalendarController = require('web.CalendarController');
    var FeedbackSnackbar = require('pivotino_feedback.feedback_snackbar');
    var session = require('web.session');

    CalendarController.include({
        _onQuickCreate: function (event) {
            var self = this;
            var proms = [];

            this._super.apply(this, arguments);

            if (self.modelName === 'calendar.event' && self.viewType === 'calendar') {
                this._rpc({
                    model: 'res.users',
                    method: 'check_calendar_feedback',
                    args: [[session.uid]],
                }).then(function (val) {
                    if (val) {
                        if (self.feedback_wizard) {
                            self.feedback_wizard.destroy();
                        }
                        var option = "Calendar Creation";
                        var value = "Managing dates has become much simpler with Pivotino?";
                        self.feedback_wizard = new FeedbackSnackbar(self, option, value);
                        var $action_manager = document.querySelector('.o_action_manager');
                        proms.push(self.feedback_wizard.insertAfter($action_manager));
                        return Promise.all(proms);
                    } else {
                        return;
                    }
                });
            }
        },
    });
});