odoo.define('pivotino_user_guide.create_product', function(require) {
    "use strict";

    var core = require('web.core');
    var tour = require('web_tour.tour');
    var _t = core._t;

    tour.register('create_product', {
        url: "/web",
        pivotino_tour: true,
        display_name: 'Create Product',
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
        content: _t("Ready to manage your product? Your <b>all product </b> can be found here, under the <b>Sales</b> app."),
        position: 'bottom',
        edition: 'community',
    }, {
        trigger: "a[data-menu-xmlid='sale.product_menu_catalog']",
        content: _t("Click here to <b> open product </b> menu to create new product"),
        position: "bottom",
    }, {
        trigger: "a[data-menu-xmlid='sale.menu_product_template_action']",
        content: _t("Click this menu to <b> see all product.</b>"),
        position: "right",
    }, {
        trigger: ".o-kanban-button-new",
        content: _t("Click here to <b> create new product.</b>"),
        position: "bottom",
    }, {
        trigger: ".o_input[name='name']",
        content: _t("<b> Choose a name</b> for your product, example: <i>'Apple'</i>"),
        position: "right",
    }, {
        trigger: ".o_input[name='list_price']",
        content: _t("Enter the <b>sales price for your product.</b>"),
        position: "right",
    }, {
        trigger: ".o_form_button_save",
        content: _t("Click here to <b> save your product.</b> <br/><br/> Congratulations, You are successfull Created New Product."),
        position: "bottom",
        edition: 'community'
    }]);
});
