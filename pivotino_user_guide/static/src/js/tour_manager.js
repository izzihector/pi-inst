odoo.define('pivotino_user_guide.TourManager', function (require) {
    "use strict";

    var core = require('web.core');
    var TourManager = require('web_tour.TourManager');
    var _t = core._t;

    /**
     * Registers a tour described by the following arguments *in order*
     *
     * @param {string} name - tour's name
     * @param {Object} [options] - options (optional), available options are:
     * @param {boolean} [options.test=false] - true if this is only for tests
     * @param {boolean} [options.skip_enabled=false]
     *        true to add a link in its tips to consume the whole tour
     * @param {string} [options.url]
     *        the url to load when manually running the tour
     * @param {boolean} [options.rainbowMan=true]
     *        whether or not the rainbowman must be shown at the end of the tour
     * @param {Promise} [options.wait_for]
     *        indicates when the tour can be started
     * @param {Object[]} steps - steps' descriptions, each step being an object
     *                     containing a tip description
     * @param {boolean} [options.pivotino_tour]
     *        whether or not the pivotino tour
     * @param {string} [options.display_name]
     *        the display name for the tour
     * @param {string} [options.tour_type]
     *        the types of tour, valid options are...
     *        onScreen0  -  Get Started
     *        onScreen1  -  On Screen Guide
     *        onScreen2  -  User Guide (PDFs)
     *        onScreen3  -  Video Guide
     */
    TourManager.include({
        register: function() {
            var args = Array.prototype.slice.call(arguments);
            var last_arg = args[args.length - 1];
            var name = args[0];
            if (this.tours[name]) {
                console.warn(_.str.sprintf("Tour %s is already defined", name));
                return;
            }
            var options = args.length === 2 ? {} : args[1];
            var steps = last_arg instanceof Array ? last_arg : [last_arg];
            var tour = {
                name: name,
                steps: steps,
                url: options.url,
                rainbowMan: options.rainbowMan === undefined ? true : !!options.rainbowMan,
                test: options.test,
                wait_for: options.wait_for || Promise.resolve(),
                // Pivotino: Added Display Name, Tour Type & Tour Summary
                pivotino_tour: options.pivotino_tour,
                display_name: options.display_name,
                tour_type: options.tour_type,
                tour_summary: options.tour_summary,
            };
            if (options.skip_enabled) {
                tour.skip_link = '<p><span class="o_skip_tour">' + _t('Skip tour') + '</span></p>';
                tour.skip_handler = function (tip) {
                    this._deactivate_tip(tip);
                    this._consume_tour(name);
                };
            }
            this.tours[name] = tour;
        },

        /**
         * Auto Show Tip Info until User hove over it
         *
         * @override
         */
        _activate_tip: function(tip, tour_name, $anchor) {
            this._super.apply(this, arguments);
            tip.widget._to_info_mode();
        },
    });

});
