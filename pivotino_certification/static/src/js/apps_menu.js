odoo.define('pivotino_certification.AppsMenu', function(require) {
    "use strict";

    var config = require('web.config');
    if (!config.device.isMobile) {
        return;
    }

    var AppsMenu = require('web.AppsMenu');

    AppsMenu.include({
        /*
        * Inherit and return only selected applications
        */
        getApps: function () {
            var default_apps = this._super.apply(this, arguments);
            var target = ["Calendar", "Contacts", "CRM"];
            var pivo_apps = [];
            for (var i = 0; i < default_apps.length; i++) {
                if (target.includes(default_apps[i].name)) {
                    pivo_apps.push(default_apps[i]);
                }
            }
            return pivo_apps;
        },
    });
});