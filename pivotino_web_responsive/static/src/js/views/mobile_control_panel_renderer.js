odoo.define('pivotino_web_responsive.MobileControlPanelRenderer', function (require) {
    "use strict";

    var ControlPanelRenderer = require('web.ControlPanelRenderer');

    ControlPanelRenderer.include({
        /*
        * Override to load searchBar only after .o_mobile_search_header
        */
        _renderSearchviewInput: function () {
//            if (!this.withBreadcrumbs || (this.$('.o_toggle_searchview_full').is(':visible') && !this.$('.o_mobile_search').is(':visible'))) {
//                this.$('.o_toggle_searchview_full').toggleClass('btn-secondary', !!this.state.query.length);
//                this.searchBar.$el.detach().insertAfter(this.$('.o_mobile_search'));
//            } else {
//                this.searchBar.$el.detach().insertAfter(this.$('.o_mobile_search_header'));
//            }
            this.searchBar.$el.detach().insertAfter(this.$('.o_mobile_search_header'));
        },

        /*
        Override the toggle mobile search view function
        */
        _toggleMobileSearchView: function () {
            this.$('.o_mobile_search').toggleClass('o_hidden');
            // disable the below _renderSearchviewInput function
            //this._renderSearchviewInput();

            // hide the header and footer of pop-up window to avoid stack issue
            var $header = $('.modal-header');
            var $footer = $('.modal-footer');
            if (!$header.hasClass('d-none')) {
                $header.addClass('d-none');
                $footer.addClass('d-none');
            } else {
                $header.removeClass('d-none');
                $footer.removeClass('d-none');
            }
        },
    });
});