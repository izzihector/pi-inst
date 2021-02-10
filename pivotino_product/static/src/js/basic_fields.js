odoo.define('pivotino_product.basic_fields', function (require) {
    "use strict";

    var basic_fields = require('web.basic_fields');
    var BooleanToggle = basic_fields.BooleanToggle;

    BooleanToggle.include({

        _onClick: function (event) {
            event.stopPropagation();

            if (this.model === 'res.currency' && this.value === false) {
                var msg = 'Please update the exchange rate for the currency that is currently being activated';
                alert(msg);
            }
            
            this._setValue(!this.value);
            this.$el.closest(".o_data_row").toggleClass('text-muted', this.value);
        },

    });
});
