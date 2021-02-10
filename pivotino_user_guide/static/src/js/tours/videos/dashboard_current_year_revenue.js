odoo.define('pivotino_user_guide.dashboard_current_year_revenue', function(require) {
    "use strict";

    var core = require('web.core');
    var tour = require('web_tour.tour');
    var _t = core._t;

    tour.register('dashboard_current_year_revenue', {
        url: "https://www.youtube.com/embed/LTPj3Qh5ZSY?rel=0",
        pivotino_tour: true,
        display_name: 'Current Year Revenue Analysis Dashboard',
        tour_summary: 'Tag line for this Tour',
        tour_type: 'onScreen3',
    }, []);

});
