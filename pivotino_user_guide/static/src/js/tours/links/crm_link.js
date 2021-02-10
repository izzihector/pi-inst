odoo.define('pivotino_user_guide.crm_link', function(require) {
    "use strict";

    var core = require('web.core');
    var tour = require('web_tour.tour');
    var _t = core._t;

    tour.register('crm_link', {
        url: "https://pivotino.com/pivotino/docs/crm",
        pivotino_tour: true,
        display_name: 'CRM',
        tour_summary: 'Tag line for this Tour',
        tour_type: 'onScreen2',
    }, []);

});
