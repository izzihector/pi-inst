odoo.define('pivotino_feedback_crm.KanbanController', function (require) {
    "use strict";

    var config = require('web.config');

    if (config.device.isMobile) {
        return;
    }

    var KanbanController = require('web.KanbanController');
    var FeedbackSnackbar = require('pivotino_feedback.feedback_snackbar');
    var session = require('web.session');

    KanbanController.include({

        _onQuickCreateRecord: function (ev) {
            var self = this;
            var proms = [];

            this._super.apply(this, arguments);

            if (self.modelName === 'crm.lead' && self.viewType === 'kanban') {
                this._rpc({
                    model: 'res.users',
                    method: 'check_crm_feedback',
                    args: [[session.uid]],
                }).then(function (val) {
                    if (val) {
                        if (self.feedback_wizard) {
                            self.feedback_wizard.destroy();
                        }
                        var option = "Opportunity Creation";
                        var value = "You are creating more leads,that's great! Are you satisfied with the lead creation steps in Pivotino?";
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