odoo.define('pivotino_user_guide.dashboard_actual_vs_target', function(require) {
    "use strict";

    var core = require('web.core');
    var tour = require('web_tour.tour');
    var _t = core._t;

    tour.register('dashboard_actual_vs_target', {
        url: "https://www.youtube.com/embed/Tosa9ndExn8?rel=0",
        pivotino_tour: true,
        display_name: 'Actual vs Target Dashboard',
        tour_summary: 'Tag line for this Tour',
        tour_type: 'onScreen3',
    }, []);

});
