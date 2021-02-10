odoo.define('pivotino_user_guide.starter_kit_sp', function(require) {
    "use strict";

    var core = require('web.core');
    var tour = require('web_tour.tour');
    var _t = core._t;

    tour.register('starter_kit_sp', {
        url: "https://www.youtube.com/embed/YmPHqkIZLT8?rel=0",
        pivotino_tour: true,
        display_name: 'Sales Person Starter Kit',
        tour_summary: 'Tag line for this Tour',
        tour_type: 'onScreen3',
    }, []);

});
