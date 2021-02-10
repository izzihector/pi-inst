odoo.define('pivotino_user_guide.DisableTour', function (require) {
    "use strict";

    var TourManager = require('web_tour.TourManager');
    var Tour = require('web_tour.tour');

    TourManager.include({
        /**
         * Disables all tours @ beginning
         *
         * @override
         */
        _register: function (do_update, tour, name) {
            // Consuming all tours from the start
            var self = this;
            var all_tours = Tour.tours;
            _.each(all_tours, function (val, key) {
                self.consumed_tours.push(key);
            });
            return this._super.apply(this, arguments);
        },
    });

});
