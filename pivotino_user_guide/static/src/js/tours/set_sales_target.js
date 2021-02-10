odoo.define('pivotino_user_guide.set_sales_target', function(require) {
    "use strict";

    var core = require('web.core');
    var tour = require('web_tour.tour');
    var _t = core._t;

    tour.register('set_sales_target', {
        url: "/web",
        pivotino_tour: true,
        display_name: 'Set Sales Target (Business Owner Only)',
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
        content: _t("Ready to manage Your Sales Target? You <b>can found monthly sales target</b>, under the <b>Sales</b> app."),
        position: 'bottom',
    }, {
        trigger: "a[data-menu-xmlid='pivotino_crm.menu_sale_target_sales']",
        content: _t("Click here to <b> configure monthly sales target.</b>"),
        position: "bottom",
    }, {
        trigger: ".o_list_button_add",
        content: _t("Click here to <b> add new sales target.</b>"),
        position: "bottom",
    }, {
        trigger: ".o_input[name='target_month']",
        content: _t("<b> Choose a month</b> for your sales target."),
        position: "top",
    }, {
        trigger: ".o_list_view a[role='button']",
        content: _t("Click here to <b>add sales person.</b>"),
        position: "bottom",
    }, {
        trigger: ".o_field_widget[name='user_id']",
        content: _t("Click here to select <b>sales person from the list.</b>"),
        position: "bottom",
    }, {
        trigger: ".o_field_widget[name='target_sales']",
        content: _t("Enter the <b>target amount</b>"),
        position: "bottom",
    }, {
        trigger: ".o_form_button_save",
        content: _t("Click here to <b> save sales target.</b> <br/> Congratulations, You are successfull <b> set the monthly sales target.</b>"),
        position: "bottom",
        edition: 'community',

    }]);
});

