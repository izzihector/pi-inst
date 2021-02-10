odoo.define('pivotino_web_responsive.relational_fields', function (require) {
    "use strict";

    var config = require('web.config');
    if (!config.device.isMobile) {
        return;
    }

    var core = require('web.core');
    var relational_fields = require('web.relational_fields');

    var FieldStatus = relational_fields.FieldStatus;
    var FieldMany2One = relational_fields.FieldMany2One;

    var qweb = core.qweb;

    var _t = core._t;

    /*
    Render new qweb view for status bar
    */
    FieldStatus.include({
        _render: function () {
            this.$el.html(qweb.render("StatusView.Mobile", {
                states: this.status_information,
                // findWhere to get a list of element that matches the condition
                status: _.findWhere(this.status_information, {selected: true}),
                clickable: this.isClickable,
            }));
        }
    });

    FieldMany2One.include({
        /*
        Make the m2o fields readonly for mobile devices
        */
        start: function () {
            var result = this._super.apply(this, arguments);
            this.$input.prop('readonly', true);
            return result;
        },

        /*
        Disable autocomplete in mobile devices
        */
        _bindAutoComplete: function () {
            if (!config.device.isMobile) {
                return this._super.apply(this, arguments);
            }
        },

        _getSearchCreatePopupOptions: function () {
            var self = this;
            var searchCreatePopupOptions = this._super.apply(this, arguments);
            _.extend(searchCreatePopupOptions, {
                selectionMode: true,
                // add on_reset func to clear the selected input
                on_reset: function () {
                    self.reinitialize(false);
                },
            });
            return searchCreatePopupOptions;
        },

        _getMobileSearch: function(search_val, context, domain) {
            var self = this;
            return new Promise(function (resolve, reject) {
                var promise;

                if (search_val !== '') {
                    promise = self._rpc({
                        model: self.field.relation,
                        method: 'name_search',
                        kwargs: {
                            name: search_val,
                            args: domain,
                            operator: "ilike",
                            limit: self.SEARCH_MORE_LIMIT,
                            context: context,
                        },
                    });
                }

                Promise.resolve(promise).then(function (results) {
                    var dynamicFilters;
                    if (results) {
                        var ids = _.map(results, function (x) {
                            return x[0];
                        });
                        // dynamicFilters = [{
                        //     description: _.str.sprintf(_t('Quick search: %s'), search_val),
                        //     domain: [['id', 'in', ids]],
                        // }];
                        dynamicFilters = []
                    }
                    self._searchCreatePopup("search", false, {}, dynamicFilters);
                });
            });
        },

        /*
        * Override to open search pop up
        */
        _search: function (search_val) {
            var self = this;
            var context = self.record.getContext(self.recordParams);
            var domain = self.record.getDomain(self.recordParams);

            // Add the additionalContext
            _.extend(context, self.additionalContext);

            // get blacklist ids if any
            var blacklisted_ids = self._getSearchBlacklist();
            if (blacklisted_ids.length > 0) {
                domain.push(['id', 'not in', blacklisted_ids]);
            }

            var mobile_def = this._getMobileSearch(search_val, context, domain);

            this.orderer.add(mobile_def);
            return mobile_def;
        },

        /*
        Override the onInputClick function to pop up search for mobile
        */
        _onInputClick: function () {
            return this._search();
        },
    });
});