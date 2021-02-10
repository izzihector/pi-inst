odoo.define('pivotino_mobile.ChangePassword', function (require) {
    "use strict";

    var ChangePassword = require('web.ChangePassword');
    var core = require('web.core');
    var web_client = require('web.web_client');

    var _t = core._t;

    ChangePassword.include({
        /*
        * Override
        */
        start: function () {
            var self = this;
            web_client.set_title(_t("Change Password"));
            var $button = self.$('.oe_form_button');
            $button.appendTo(this.getParent().$footer);
            $button.eq(1).click(function () {
                self.$el.parents('.modal').modal('hide');
            });
            $button.eq(0).click(function () {
                self._rpc({
                    route: '/web/session/change_password',
                    params: {
                        fields: $('form[name=change_password_form]').serializeArray()
                    }
                }).then(function (result) {
                    if (result.error) {
                        self._display_error(result);
                    } else {
                        if (window.pivotinoMobile &&
                            window.pivotinoMobile.nativeWebView &&
                            window.pivotinoMobile.nativeWebView === 'nativeWebView') {
                            var url = '/nativeAppLogout';
                            window.location.href = url;
                        } else {
                            self.do_action('logout');
                        }
                    }
                });
            });
        },
    });
});