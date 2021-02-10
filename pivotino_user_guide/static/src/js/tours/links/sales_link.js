odoo.define('pivotino_user_guide.sales_link', function(require) {
    "use strict";

    var core = require('web.core');
    var tour = require('web_tour.tour');
    var _t = core._t;

    tour.register('sales_link', {
        url: "https://pivotino.com/pivotino/docs/sales",
        pivotino_tour: true,
        display_name: 'Sales',
        tour_summary: 'Tag line for this Tour',
        tour_type: 'onScreen2',
    }, []);

});
