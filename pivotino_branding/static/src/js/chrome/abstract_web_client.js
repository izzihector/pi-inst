odoo.define('pivotino_branding.AbstractWebClient', function (require) {
"use strict";

    var AbstractWebClient = require('web.AbstractWebClient');
    var core = require('web.core');
    var _t = core._t;

    AbstractWebClient.include({
        init: function (parent) {
            var self = this;
            this._super.apply(this, arguments)
            // Change window title to Pivotino
            this.set('title_part', {"zopenerp": "Pivotino"});
        },
    });

    // Replace 'Odoo session expired' to 'Pivotino Session Expired'
    function session_expired(cm) {
        return {
            display: function () {
                cm.show_warning({type: _t("Pivotino Session Expired"), data: {message: _t("Your Session expired. Please refresh the current web page.")}});
            }
        };
    }
    core.crash_registry.add('odoo.http.SessionExpiredException', session_expired);

});
