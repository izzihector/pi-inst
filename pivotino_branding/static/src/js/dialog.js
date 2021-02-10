odoo.define('pivotino_branding.Dialog', function (require) {
    'use strict';

    var core = require('web.core');
    var Dialog = require('web.Dialog');

    var _t = core._t;

    Dialog.include({
        init: function (parent, options) {
            var self = this;
            this._super.apply(this, arguments)
            // Change dialog title to Pivotino if the title is Odoo
            if (options.title == 'Odoo') {
                this.title = 'Pivotino';
            } else {
                this.title = options.title;
            }
        }
    });

});