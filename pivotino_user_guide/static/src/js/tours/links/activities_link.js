odoo.define('pivotino_user_guide.activities_link', function(require) {
    "use strict";

    var core = require('web.core');
    var tour = require('web_tour.tour');
    var _t = core._t;

    tour.register('activities_link', {
        url: "https://pivotino.com/pivotino/docs/activities",
        pivotino_tour: true,
        display_name: 'Activities Dashboard',
        tour_summary: 'Tag line for this Tour',
        tour_type: 'onScreen2',
    }, []);

});
