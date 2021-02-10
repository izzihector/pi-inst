odoo.define('pivotino_crm.KanbanRenderer', function (require) {
    "use strict";

    var KanbanRenderer = require('web.KanbanRenderer');

    KanbanRenderer.include({
        _renderGrouped: function (fragment) {
            var self = this;
            this._super.apply(this, arguments);
            // disable the group sorting for crm.lead
            if (self.groupedByM2O && self.state.model === 'crm.lead') {
                self.$el.sortable('destroy');
            }
        },
    });
});