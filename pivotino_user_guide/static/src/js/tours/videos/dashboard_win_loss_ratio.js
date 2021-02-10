odoo.define('pivotino_user_guide.dashboard_win_loss_ratio', function(require) {
    "use strict";

    var core = require('web.core');
    var tour = require('web_tour.tour');
    var _t = core._t;

    tour.register('dashboard_win_loss_ratio', {
        url: "https://www.youtube.com/embed/tfUiIZR_y6Q?rel=0",
        pivotino_tour: true,
        display_name: 'Win Loss Ratio Dashboard',
        tour_summary: 'Tag line for this Tour',
        tour_type: 'onScreen3',
    }, []);

});
