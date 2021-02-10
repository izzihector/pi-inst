odoo.define('pivotino_crm.BasicController', function (require) {
"use strict";

    var BasicController = require('web.BasicController');
    var Dialog = require('web.Dialog');
    var core = require('web.core');

    var _t = core._t;

    BasicController.include({
        // inherit the _deleteRecords to show warning message when the user
        // delete sales target
        _deleteRecords: function(ids) {
            var self = this;
            function doIt() {
                return self.model
                    .deleteRecords(ids, self.modelName)
                    .then(self._onDeletedRecords.bind(self, ids));
            }
            // change the warning message if the current model is sale.target
            if (this.modelName === 'sale.target'){
                Dialog.confirm(this, _t("Deleting sales target record(s) will affect the dashboard summary. Click 'Ok' if you wish to proceed with deleting the sales target record(s)."), {
                    confirm_callback: doIt,
                });
            } else {
                this._super.apply(this, arguments);
            }
        },
    });
});