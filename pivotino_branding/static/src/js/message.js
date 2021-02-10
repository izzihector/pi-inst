odoo.define('pivotino_branding.Message', function (require) {
    "use strict";

    var Message = require('mail.model.Message');

    Message.include({
        /*
        * Override for odoo de-branding
        */
        getAvatarSource: function () {
            if (this._isOdoobotAuthor()) {
                return '/pivotino_branding/static/src/img/bot.png';
            } else if (this.hasAuthor()) {
                return '/web/image/res.partner/' + this.getAuthorID() + '/image_128';
            } else if (this.getType() === 'email') {
                return '/mail/static/src/img/email_icon.png';
            }
            return '/mail/static/src/img/smiley/avatar.jpg';
        },
        /*
        * Override for odoo de-branding
        */
        _getAuthorName: function () {
            if (this._isOdoobotAuthor()) {
                return "PivotinoBot";
            }
            return this._super.apply(this, arguments);
        },
    });
});