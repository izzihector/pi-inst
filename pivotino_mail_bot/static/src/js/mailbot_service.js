odoo.define('pivotino_mail_bot.MailBotService', function (require) {
"use strict";

    var MailBotService = require('mail_bot.MailBotService');

    MailBotService.include({
        // override this function to return nothing to the preview message
        getPreviews: function (filter) {
            return []
        },
    });
});