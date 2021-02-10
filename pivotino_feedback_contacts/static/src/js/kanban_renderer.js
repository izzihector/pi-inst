odoo.define('pivotino_feedback_contacts.KanbanRenderer', function (require) {
    "use strict";

    var config = require('web.config');

    if (config.device.isMobile) {
        return;
    }

    var KanbanRenderer = require('web.KanbanRenderer');
    var FeedbackSnackbar = require('pivotino_feedback.feedback_snackbar');
    var session = require('web.session');

    KanbanRenderer.include({
        _renderView: function () {
            var self = this;
            var proms = [];

            // remove snackbar if there is any existing
            var snackbar = document.querySelector('.feedback_snackbar_root');
            if (snackbar) {
                snackbar.remove();
            }

            if (self.state.model === 'res.partner' && self.viewType === 'kanban') {
                this._rpc({
                    model: 'res.users',
                    method: 'check_contact_feedback',
                    args: [[session.uid]],
                }).then(function (val) {
                    if (val) {
                        if (self.feedback_wizard) {
                            self.feedback_wizard.destroy();
                        }
                        var option = "Contacts Creation";
                        var value = "You are adding more contacts,that's great! Are you satisfied with the contact creation steps in Pivotino?";
                        self.feedback_wizard = new FeedbackSnackbar(self, option, value);
                        var $action_manager = document.querySelector('.o_action_manager');
                        proms.push(self.feedback_wizard.insertAfter($action_manager));
                        return Promise.all(proms);
                    } else {
                        return;
                    }
                });
            }

            return this._super.apply(this, arguments);
        },
    });
});