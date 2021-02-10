odoo.define('pivotino_feedback.systray', function (require) {
    "use strict";

    var config = require('web.config');
    var core = require('web.core');
    var SystrayMenu = require('web.SystrayMenu');
    var Widget = require('web.Widget');
    var FeedbackPopUp = require('pivotino_general_feedback.feedback_popup');
    var Dialog = require('web.Dialog');

    var QWeb = core.qweb;
    var _t = core._t;

    var FeedbackActionMenu = Widget.extend({
        sequence: 40,
        template: 'pivotino_feedback.pivotino_feeedback_icon',
        events: {
            'click .btn-wizard': '_onClickOpenFeedback',
        },

        start: function (parent) {
            return this._super.apply(this, arguments);
        },
        _onClickOpenFeedback: function () {
            var self = this;
            var proms = [];

            if (self.feedback_wizard) {
                self.feedback_wizard.destroy();
            }

            return self._rpc({
                model: 'general.feedback.tags',
                method: 'get_tags_object',
                args: [],
            }).then(function (result) {
                // Pre-defined values for tags
                var positive = result[0];
                var negative = result[1];
                self.feedback_wizard = new FeedbackPopUp(self, positive, negative);
                var $action_manager = document.querySelector('.o_action_manager');
                proms.push(self.feedback_wizard.insertAfter($action_manager));
                return Promise.all(proms);
            });
        }
    });

    SystrayMenu.Items.push(FeedbackActionMenu);
    return FeedbackActionMenu;
});
