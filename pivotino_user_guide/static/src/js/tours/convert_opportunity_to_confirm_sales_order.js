odoo.define('pivotino_user_guide.convert_opportunity_to_confirm_sales_order', function(require) {
    "use strict";

    var core = require('web.core');
    var tour = require('web_tour.tour');
    var _t = core._t;

    tour.register('cconvert_opportunity_to_confirm_sales_order', {
        url: "/web",
        pivotino_tour: true,
        display_name: 'Convert Opportunity to Confirm Sales Order',
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
        trigger: ".o_lead_opportunity_form .o_field_date",
        content: _t("Confirm your <b>Expected Closing Date</b> for This opportunity."),
        position: "top",
    }, {
        trigger: ".o_cp_left .o_form_button_save",
        content: _t("Save this opportunity</b>."),
        position: "right",
    }, {
        trigger: ".o_lead_opportunity_form .btn.btn-primary",
        content: _t("Click here to <b>create new quotation</b> from opportunity."),
        position: "bottom",
    }, {
        trigger: ".o_field_x2many_list_row_add a",
        content: _t("Click here to <b>add product</b> in quotation."),
        position: "bottom",
    }, {
        trigger: ".o_cp_left .o_form_button_save",
        content: _t("Save this opportunity</b>."),
        position: "right",
    }, {
        trigger: ".o_form_readonly .btn.btn-secondary[name='action_confirm']",
        content: _t("Click here to <b>confirm</b> your quotation."),
        position: "bottom",
    }, {
        trigger: "ol.breadcrumb li.breadcrumb-item:nth-child(2)",
        // extra_trigger: '.o_lead_opportunity_form',
        content: _t("Use the breadcrumbs to <b>go back to your opportunity</b> <br/> See the <b>status of your opportunity. </b> It's Won. <br/> Good job! You completed the tour of Convert Opportunity to Confirm Sales."),
        position: "bottom",
        edition: 'community',
    }]);
});
