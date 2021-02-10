odoo.define('pivotino_user_guide.starter_kit_bo', function(require) {
    "use strict";

    var core = require('web.core');
    var tour = require('web_tour.tour');
    var _t = core._t;

    tour.register('starter_kit_bo', {
        url: "https://www.youtube.com/embed/LXrAu8GcRNI?rel=0",
        pivotino_tour: true,
        display_name: 'Business Owner Starter Kit',
        tour_summary: 'Tag line for this Tour',
        tour_type: 'onScreen3',
    }, []);

});
