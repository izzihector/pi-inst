odoo.define('pivotino_web_responsive.view_dialogs', function (require) {
    "use strict";

    var config = require('web.config');
    if (!config.device.isMobile) {
        return;
    }

    var core = require('web.core');
    var view_dialogs = require('web.view_dialogs');
    var SelectCreateDialog = view_dialogs.SelectCreateDialog;

    var _t = core._t;

    SelectCreateDialog.include({
        /*
        * Override init func for mobile change initial view
        */
        init: function () {
            this._super.apply(this,arguments);
            this.on_reset = this.options.on_reset || (function () {});
            this.viewType = 'kanban';
        },

        /*
        * Override and prepare buttons for mobile m2o dropdown
        * all button name in capital letter
        */
        _prepareButtons: function () {
            var self = this;
            this.__buttons = [];
            if (this.options.disable_multiple_selection) {
                if (this.options.selectionMode)  {
                    this.__buttons.push({
                        text: _t("CLEAR"),
                        classes: 'btn-secondary o_reset_button',
                        close: true,
                        click: function () {
                            this.on_reset();
                        },
                    });
                }
            }
            if (!this.options.no_create) {
                this.__buttons.unshift({
                    text: _t("CREATE"),
                    classes: 'btn-primary',
                    click: this.create_edit_record.bind(this)
                });
            }
        },
    });
});