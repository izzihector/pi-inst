odoo.define('pivotino_user_guide.create_sales_quotation', function(require) {
    "use strict";

    var core = require('web.core');
    var tour = require('web_tour.tour');
    var _t = core._t;

    tour.register('create_sales_quotation', {
        url: "/web",
        pivotino_tour: true,
        display_name: 'Create Sales Quotation',
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
        content: _t("Ready to manage Your Sales Quotation? You <b>can found all sales quotation</b>, under the <b>Sales</b> app."),
        position: 'bottom',
    }, {
        trigger: "a[data-menu-xmlid='sale.sale_order_menu']",
        content: _t("Click here and <b> choose the quotation menu.</b>"),
        position: "bottom",
    }, {
        trigger: "a[data-menu-xmlid='sale.menu_sale_quotations']",
        content: _t("Click here to <b> see all your quotation.</b>"),
        position: "right",
    }, {
        trigger: ".o_list_button_add",
        content: _t("Click here to <b> add new quotation.</b>"),
        position: "bottom",
    }, {
        trigger: ".o_field_widget[name='partner_id']",
        content: _t("Click here and <b> Choose the customer</b> from the list."),
        position: "top",
    }, {
        trigger: ".o_field_x2many_list_row_add a",
        content: _t("Click here to <b>add product</b> in quotation."),
        position: "bottom",
    }, {
        trigger: ".o_field_widget[name='product_id']",
        content: _t("Click here to  <b>select product</b> from product list."),
        position: "bottom",
    }, {
        trigger: ".o_field_widget[name='client_order_ref']",
        content: _t("Click here to <b>customer reference</b> for quotation"),
        position: "bottom",
    }, {
        trigger: ".o_cp_left .o_form_button_save",
        content: _t("Click here to <b>save this quotation.</b> <br/><br/> Congratulations, You are successfull <b>created quotation manually.</b> <br/></br> You can <b>confirm the order</b> by clicking the <b>Confim</b> button and system will automatically create <b> opportunity </b> in <b>won</b> stage for you."),
        position: "right",
        edition: 'community',

    }]);
});

