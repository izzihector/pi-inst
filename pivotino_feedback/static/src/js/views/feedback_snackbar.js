odoo.define('pivotino_feedback.feedback_snackbar', function (require) {
    "use strict";

    var Widget = require('web.Widget');
    var session = require('web.session');

    var FeedbackSnackbar = Widget.extend({
        template: 'FeedbackSnackbar',

        events: {
            'click .snackbar_btn': '_onSnackbarButtonClick',
            'click .btn-send': '_onButtonSend',
        },

        init: function (parent, option, value) {
            var self = this;
            this._super(parent);
            this.option = option;
            this.value = value;
        },

        start: function () {
            var self = this;
            this._super.apply(this, arguments);
            // set the feedback question value
            this.$('.question_value').text(this.value);

            // get current res.users obj for home action (action_id)
            this._rpc({
                model: 'res.users',
                method: 'search_read',
                domain: [['id', '=', session.uid]],
            }).then(function (user) {
                self.currentUser = user;
            });
        },

        _onSnackbarButtonClick: function (ev) {
            var self = this;
            var url = session.origin;
            var username = session.partner_display_name;
            var feedback_val = '';

            ev.preventDefault();

            if (ev.currentTarget.id === 'agree') {
                // hide questions and show appreciation msg
                this.$('.snackbar_top').hide();
                this.$('.snackbar_appreciate').show();

                // automatically hide the snackbar after 3s
                setTimeout(function(){ self.$el.hide(); }, 3000);

                return this._rpc({
                    model: 'res.users',
                    method: 'submit_feedback',
                    args: [session.uid, url, feedback_val, this.option, true],
                });
            }
            else if (ev.currentTarget.id === 'disagree') {
                var $agree_btn = this.$('#agree');
                $agree_btn.hide();
                var $snackbar_btm = this.$('.snackbar_bottom');
                $snackbar_btm.show();
                $(ev.currentTarget).addClass('active');
            }
        },

        _onButtonSend: function(ev) {
            var self = this;
            // hide questions and show appreciation msg
            this.$('.snackbar_top').hide();
            this.$('.snackbar_bottom').hide();
            this.$('.snackbar_appreciate').show();

            // automatically hide the snackbar after 3s
            setTimeout(function(){ self.$el.hide(); }, 3000);

            var feedback_val = this.$('#feedback').val();

            var url = session.origin;
            var username = session.partner_display_name;

            return this._rpc({
                model: 'res.users',
                method: 'submit_feedback',
                args: [session.uid, url, feedback_val, this.option, false],
            });
        },
    });

    return FeedbackSnackbar;
});