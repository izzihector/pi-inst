odoo.define('pivotino_branding.systray.MessagingMenu', function (require) {
    "use strict"

    var MessagingMenu = require('mail.systray.MessagingMenu');
    var core = require('web.core');

    var _t = core._t;

    MessagingMenu.include({
        /*
        * Override for de-branding
        */
        _handleResponseNotificationPermission: function (value) {
            this.call('mailbot_service', 'removeRequest');
            if (value !== 'granted') {
                this.call('bus_service', 'sendNotification', _t('Permission denied'),
                    _t('Pivotino will not have the permission to send native notifications on this device.'));
            }
            this._updateCounter();
        },
    });
});