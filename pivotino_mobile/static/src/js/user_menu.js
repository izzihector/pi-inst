odoo.define('pivotino_mobile.UserMenu', function (require) {
    "use strict";

    var UserMenu = require('web.UserMenu');

    UserMenu.include({
        /**
         * @override
         */
        start: function () {
            var self = this;
            this._super.apply(this, arguments);

            // Hide/Show Logout Menu
            if (window.pivotinoMobile &&
              window.pivotinoMobile.nativeWebView &&
              window.pivotinoMobile.nativeWebView === 'nativeWebView') {
                this.$el.find('a.logout-pivotino-web').addClass('d-none');
                this.$el.find('a.logout-pivotino-app').removeClass('d-none');
            } else {
                this.$el.find('a.logout-pivotino-app').addClass('d-none');
                this.$el.find('a.logout-pivotino-web').removeClass('d-none');
            }
        },
    });

});
