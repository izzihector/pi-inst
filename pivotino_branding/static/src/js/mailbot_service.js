odoo.define('pivotino_branding.MailBotService', function (require) {
    "use strict";

    var MailBotService = require('mail_bot.MailBotService');
    var core = require('web.core');

    var _t = core._t;

    MailBotService.include({
        /*
        * Inherit and modify the title of getPreviews
        */
        getPreviews: function (filter) {
            var previews = this._super.apply(this, arguments);
            if (previews.length > 0) {
                previews[0]['title'] = _t("PivotinoBot has a request");
                previews[0]['imageSRC'] = "/pivotino_branding/static/src/img/bot.png";
            }
            return previews;
        },
    });
});