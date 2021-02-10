odoo.define('pivotino_user_guide.dashboard_sales_cycle_length', function(require) {
    "use strict";

    var core = require('web.core');
    var tour = require('web_tour.tour');
    var _t = core._t;

    tour.register('dashboard_sales_cycle_length', {
        url: "https://www.youtube.com/embed/g2KYEugyKjE?rel=0",
        pivotino_tour: true,
        display_name: 'Sales Cycle Length Dashboard',
        tour_summary: 'Tag line for this Tour',
        tour_type: 'onScreen3',
    }, []);

});
