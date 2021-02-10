odoo.define('pivotino_user_guide.plan_your_activity_and_confirm_sales', function(require) {
    "use strict";

    var core = require('web.core');
    var tour = require('web_tour.tour');
    var _t = core._t;

    tour.register('plan_your_activity_and_confirm_sales', {
        url: "/web",
        pivotino_tour: true,
        display_name: 'Plan Your Activity & Confirm Sales',
        tour_summary: 'Tag line for this Tour',
        tour_type: 'onScreen1',
        'skip_enabled': true,
    }, [{
        edition: "community",
        trigger: ".o_main_navbar .o_menu_apps",
        content: _t('Click on the <i><b>Home icon</b></i> to navigate across apps.'),
        position: "bottom",
    }, {
        trigger: '.o_app[data-menu-xmlid="crm.crm_menu_root"]',
        content: _t("Ready to boost your sales? Your <b>Pipeline</b> can be found here, under the <b>CRM</b> app."),
        position: 'bottom',
        edition: 'community',
    }, {
        trigger: "a[data-menu-xmlid='crm.crm_menu_sales']",
        content: _t("Click here to <b>open your pipeline menu.</b>"),
        position: "bottom",
    }, {
        trigger: "a[data-menu-xmlid='crm.menu_crm_opportunities']",
        content: _t("Click here to <b> open your opportunity pipeline.</b>"),
        position: "right",
    }, {
        trigger: ".o-kanban-button-new",
        extra_trigger: '.o_opportunity_kanban',
        content: _t("Click here to <b>create your opportunity</b> and add it to your pipeline."),
        position: "bottom",
    }, {
        trigger: ".o_kanban_quick_create input:first",
        content: _t("<b>Choose a name</b> for your opportunity, example: <i>'Need a new website'</i>"),
        position: "right",
    }, {
        trigger: ".o_kanban_quick_create div.o_input_dropdown",
        content: _t("<b>Choose a partner (optional)</b> for your opportunity, example: <b>Onnet Sdn Bhd</b>"),
        position: "right",
    }, {
        trigger: ".o_kanban_quick_create .o_field_float",
        content: _t("<b>Enter the expected revenue</b> of your opportunity, example: <b>25000 EURO</b>"),
        position: "right",
    }, {
        trigger: ".o_kanban_quick_create .o_kanban_edit",
        content: _t("Click here to <b>edit your opportunity</b>."),
        position: "bottom",
    }, {
        trigger: ".o_chatter_button_schedule_activity",
        content: _t("Let's schedule an activity."),
        position: "top"
    }, {
        trigger: ".o_field_many2one[name='activity_type_id']",
        content: _t("Choose an <b>activity type.</b>"),
        position: "top",
    }, {
        trigger: ".o_field_date[name='date_deadline']",
        content: _t("Select <b>the due date </b>for your activity."),
        position: "left",
    }, {
        trigger: ".o_field_many2one.o_with_button[name='user_id']",
        content: _t("Select <b>the PIC </b>for your activity"),
        position: "left",
    }, {
        trigger: ".btn.btn-primary[name='action_close_dialog']",
        content: _t("Click her to <b>Schedule your activity</b>."),
        position: "top",
    }, {
        trigger: ".o_cp_left .o_form_button_save",
        content: _t("Save this opportunity</b>."),
        position: "right",
    }, {
        trigger: ".btn.btn-primary[name='action_sale_quotations_new']",
        content: _t("Click here to <b>create new quotation</b> from opportunity."),
        position: "bottom",
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
        content: _t("Click here to <b>save this quotation.</b>"),
        position: "right",
    }, {
        trigger: ".o_form_readonly .btn.btn-secondary[name='action_confirm']",
        content: _t("Click here to <b>confirm</b> your quotation. <br/> Good job! You completed the tour <b>Plan Activity & Confirm Sales.</b>"),
        position: "bottom",
    }, {
        trigger: "ol.breadcrumb li.breadcrumb-item:nth-child(2)",
        content: _t("Use the breadcrumbs to <b>go back to your opportunity</b> and <br/> See the <b>status of your opportunity. It's Won.</b>"),
        position: "bottom",
        edition: 'community',

    }]);
});
