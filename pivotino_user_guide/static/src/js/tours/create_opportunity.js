odoo.define('pivotino_user_guide.create_opportunity', function(require) {
    "use strict";

    var core = require('web.core');
    var tour = require('web_tour.tour');
    var _t = core._t;

    tour.register('create_opportunity', {
        url: "/web",
        pivotino_tour: true,
        display_name: 'Create Opportunity',
        tour_summary: 'Tag line for this Tour',
        tour_type: 'onScreen0',
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
        content: _t("Click here to <b>create your first opportunity</b> and add it to your pipeline."),
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
        trigger: ".o_kanban_quick_create .o_kanban_add",
        content: _t("Click here to <b>add your opportunity</b>. <br/> </br> Once you finished the first activity of opportunity, <br/> you can <b> Drag &amp; drop opportunities</b> between columns as you progress in your sales cycle. <br/> <br/> Congratulations! <b> You completed the tour of Create Opportunity with Drag and Drop.</b>"),
        position: "bottom",
        edition: 'community',

    }]);
});












    //     trigger: ".o_kanban_quick_create .o_kanban_edit",
    //     content: _t("Click here to <b>edit your opportunity</b>."),
    //     position: "bottom",
    // }, {
    //     trigger: ".o_lead_opportunity_form .o_field_date",
    //     content: _t("Confirm your <b>Expected Closing Date</b> for This opportunity."),
    //     position: "top",
    // }, {
    //     trigger: ".o_cp_left .o_form_button_save",
    //     content: _t("Save this opportunity</b>."),
    //     position: "right",
    // }, {
    //     trigger: ".breadcrumb-item:not(.active):last",
    //     extra_trigger: '.o_lead_opportunity_form',
    //     content: _t("Use the breadcrumbs to <b>go back to your sales pipeline</b> <br/> Good job! You completed the tour of Create Opportunity."),
    //     position: "bottom",
    // }, {
    //     trigger: ".o_opportunity_kanban .o_kanban_group:first-child .o_kanban_record:first()",
    //     content: _t("<b>Drag &amp; drop opportunities</b> between columns as you progress in your sales cycle."),
    //     position: "right",
    //     run: "drag_and_drop .o_opportunity_kanban .o_kanban_group:eq(1) ",
    //     edition: 'community',
