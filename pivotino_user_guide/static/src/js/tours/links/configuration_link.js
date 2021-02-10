odoo.define('pivotino_user_guide.configuration_link', function(require) {
    "use strict";

    var core = require('web.core');
    var tour = require('web_tour.tour');
    var _t = core._t;

    tour.register('configuration_link', {
        url: "https://pivotino.com/pivotino/docs/configuration",
        pivotino_tour: true,
        display_name: 'Configuration',
        tour_summary: 'Tag line for this Tour',
        tour_type: 'onScreen2',
    }, []);

});
