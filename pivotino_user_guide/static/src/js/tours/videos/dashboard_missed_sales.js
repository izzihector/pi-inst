odoo.define('pivotino_user_guide.dashboard_missed_sales', function(require) {
    "use strict";

    var core = require('web.core');
    var tour = require('web_tour.tour');
    var _t = core._t;

    tour.register('dashboard_missed_sales', {
        url: "https://www.youtube.com/embed/RW2CmIwVgPg?rel=0",
        pivotino_tour: true,
        display_name: 'Missed Sales Dashboard',
        tour_summary: 'Tag line for this Tour',
        tour_type: 'onScreen3',
    }, []);

});
