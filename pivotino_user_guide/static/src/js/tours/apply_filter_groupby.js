odoo.define('pivotino_user_guide.apply_filter_groupby', function(require) {
    "use strict";

    var core = require('web.core');
    var tour = require('web_tour.tour');
    var _t = core._t;

    tour.register('apply_filter_groupby', {
        url: "/web",
        pivotino_tour: true,
        display_name: 'Apply Filters, Group By & Save as Favorites',
        tour_summary: 'Tag line for this Tour',
        tour_type: 'onScreen1',
        'skip_enabled': true,
    }, [{
        edition: "community",
        trigger: ".o_main_navbar .o_menu_apps",
        content: _t('Click on the <i><b>Home icon</b></i> to navigate across apps.'),
        position: "bottom",
    }, {
        trigger: '.o_app[data-menu-xmlid="sale.sale_menu_root"]',
        content: _t("Ready to <b>apply filters, group by & save as favorites? </b>"),
        position: 'bottom',
        edition: 'community',
    }, {
        trigger: ".o_filters_menu_button",
        content: _t("Click here to apply <b> Filters </b> for your sales quotation."),
        position: "bottom",
    }, {
        trigger: ".o_dropdown_menu .o_menu_item a:contains(Sales Orders)",
        content: _t("The system allowed to apply any predefined filters from the list. </br> Also, you can apply custom filters by clicking on the <b> Add Custom Filter.</b> </br> example: <i>'Let's apply <b> Sales Order </b> filter. </i>"),
        position: "left",
    }, {
        trigger: ".o_dropdown_toggler_btn:contains(Group By)",
        content: _t("Click here to apply <b> Group By </b> for your sales quotation"),
        position: "bottom",
    }, {
        trigger: ".o_dropdown_menu .o_menu_item a:contains(Customer)",
        content: _t("The system allowed to apply any predefined group by from the list. </br> Also, you can apply custom group by clicking on the <b> Add Custom Group.</b> </br> example: <i>'Let's see the quotation group by <b> Customer </b>.</i>"),
        position: "left",
    }, {
        trigger: ".o_favorites_menu_button",
        content: _t("Click here to save <b> current search. </b>"),
        position: "bottom",
    }, {
        trigger: ".o_add_favorite",
        content: _t("Click here to <b> add current search.</b>"),
        position: "right",
    }, {
        trigger: ".o_favorite_name",
        content: _t("Click here to <b>enter your favorites search name.</b>"),
        position: "left",
    }, {
        trigger: ".custom-control-label:contains(Use by default)",
        content: _t("Click here to save <b> current search as default </b>"),
        position: "right",
    }, {
        trigger: ".btn.btn-primary:contains(Save)",
        content: _t("Click here to <b>save your current search.</b>.<br/> Congratulations, You are successfull <b> apply the filters, group by & save current search as a favorites.</b>"),
        position: "bottom",
        edition: 'community',

    }]);
});


