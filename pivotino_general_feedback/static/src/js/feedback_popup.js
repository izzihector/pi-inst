odoo.define('pivotino_general_feedback.feedback_popup', function (require) {
    "use strict";

    var Widget = require('web.Widget');
    var session = require('web.session');

    var FeedbackPopUp = Widget.extend({
        template: 'FeedbackGeneralPopUp',

        events: {
            'click .general_btn': '_onClickButton',
            'click .btn-cancel': '_onClickCancel',
            'click .btn-send-smile': '_onButtonPositiveSend',
            'click .btn-send-frown': '_onButtonNegativeSend',
            'click .smile_main': '_onPositiveFeedback',
            'click .frown_main': '_onNegativeFeedback',
        },

        init: function (parent, positive, negative) {
            var self = this;
            this._super(parent);
            this.positive = positive;
            this.negative = negative;
        },

        start: function () {
            var self = this;
            this._super.apply(this, arguments);

            this._rpc({
                model: 'res.users',
                method: 'search_read',
                domain: [['id', '=', session.uid]],
            }).then(function (user) {
                self.currentUser = user;
            });
        },

        _onClickButton: function (ev) {
            var self = this;
            ev.preventDefault();

            if (!ev.currentTarget.classList.contains("selected")) {
                ev.currentTarget.className += " selected";
            }
            else {
                ev.currentTarget.classList.remove("selected")
            }
        },

        _onClickCancel: function (ev) {
            var self = this;
            self.$el.hide()
        },

        _onButtonPositiveSend: function(ev) {
            var self = this;

            this.$('.happy_view').hide();
            this.$('.feedback_appreciate').show();

            var feedback_val = this.$('#pos_add_feedback').val();
            var url = session.origin;
            var tags = [];

            var all_btn = this.$('.btn-positive');

            for (var i = 0; i < all_btn.length; i++) {
                if (all_btn[i].className.includes("selected")) {
                    tags.push({'answer':'yes',
                        'code':all_btn[i].id})
                } else {
                    tags.push({'answer':'no',
                        'code':all_btn[i].id})
                }
            }

            setTimeout(function(){ self.$el.hide(); }, 3000);

            return this._rpc({
                model: 'res.users',
                method: 'submit_positive_feedback_record',
                args: [session.uid, url, feedback_val, tags],
            });

            // Comment for now ( using cron in the future )
            // return this._rpc({
            //     model: 'res.users',
            //     method: 'check_feedback_record',
            //     args: [session.uid, url, feedback_val, tags],
            // });
        },

        _onButtonNegativeSend: function(ev) {
            var self = this;

            this.$('.sad_view').hide();
            this.$('.feedback_appreciate').show();

            var feedback_val = this.$('#neg_add_feedback').val();
            console.log('WHY', feedback_val);
            var url = session.origin;
            var tags = [];

            var all_neg_btn = this.$('.btn-negative');

            for (var i = 0; i < all_neg_btn.length; i++) {
                if (all_neg_btn[i].className.includes("selected")) {
                    tags.push({'answer':'yes',
                        'code':all_neg_btn[i].id})
                } else {
                    tags.push({'answer':'no',
                        'code':all_neg_btn[i].id})
                }
            }

            setTimeout(function(){ self.$el.hide(); }, 3000);

            return this._rpc({
                model: 'res.users',
                method: 'submit_negative_feedback_record',
                args: [session.uid, url, feedback_val, tags],
            });

            // Comment for now ( using cron in the future )
            // return this._rpc({
            //     model: 'res.users',
            //     method: 'check_feedback_record',
            //     args: [session.uid, url, feedback_val, tags],
            // });
        },

        _onPositiveFeedback: function(ev) {
            var self = this;

            this.$('.main_view').hide();
            this.$('.happy_view').show();
        },

        _onNegativeFeedback: function(ev) {
            var self = this;

            this.$('.main_view').hide();
            this.$('.sad_view').show();
        }

    });

    return FeedbackPopUp;
});