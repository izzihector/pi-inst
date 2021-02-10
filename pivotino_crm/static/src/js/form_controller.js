odoo.define('pivotino_crm.FormController', function (require) {
"use strict";

    var FormController = require('web.FormController');
    var Dialog = require('web.Dialog');
    var core = require('web.core');

    var _t = core._t;

    FormController.include({
        // inherit the _onEdit to show warning message when the user trying to
        // edit past sale target
        _onEdit: function () {
            var self = this;
            if (this.modelName === 'sale.target'){
                // get the target date object
                var target_date = self.model.localData[self.handle].data.target_date._d;
                if (target_date){
                    var today = new Date();
                    // get the first date of the month, use it to compare with
                    // the target date
                    var first_date = new Date(today.getFullYear(), today.getMonth(), 1);
                    // if the first date of the current month is greater than
                    // the target date, then alert user since they are editing
                    // a past sales target
                    if (first_date > target_date) {
                        Dialog.alert(this,
                            _t("Editing PAST sales target record(s) will affect the dashboard summary. Click 'Ok' if you wish to proceed with editing the PAST sales target record(s)."),
                        );
                    }
                }
            }
            this._super.apply(this, arguments);
        },
    });
});