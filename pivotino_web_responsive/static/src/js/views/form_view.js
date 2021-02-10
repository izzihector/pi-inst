odoo.define('pivotino_web_responsive.FormView', function (require) {
    "use strict";

    var config = require('web.config');
    if (!config.device.isMobile) {
        return;
    }

    var FormView = require('web.FormView');

    FormView.include({
        /*
        * Disable the auto-focus in mobile devices
        * so that keyboard will not disrupt the view in mobilegit
        */
        init: function () {
            this._super.apply(this, arguments);
            this.controllerParams.disableAutofocus = true;
        }
    });
});