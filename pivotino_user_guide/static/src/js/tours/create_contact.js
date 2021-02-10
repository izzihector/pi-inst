odoo.define('pivotino_user_guide.create_contact', function(require) {
    "use strict";

    var core = require('web.core');
    var tour = require('web_tour.tour');
    var _t = core._t;

    tour.register('create_contact', {
        url: "/web",
        pivotino_tour: true,
        display_name: 'Create Contact',
        tour_summary: 'Tag line for this Tour',
        tour_type: 'onScreen0',
        'skip_enabled': true,
    }, [{
        edition: "community",
        trigger: ".o_main_navbar .o_menu_apps",
        content: _t('Click on the <i><b>Home icon</b></i> to navigate across apps.'),
        position: "bottom",
    }, {
        trigger: '.o_app[data-menu-xmlid="contacts.menu_contacts"]',
        content: _t("Ready to manage your Customer / Contact ? Your <b>all Customer / Contact</b> can be found here, under the <b>Contact</b> app."),
        position: 'bottom',
        edition: 'community',
    }, {
        trigger: ".o-kanban-button-new",
        extra_trigger: '.o_res_partner_kanban',
        content: _t("Click here to <b> Create Your Customer as a Company / Contact as a Individual </b> and add it to your customer / contact list."),
        position: "bottom",
    }, {
        trigger: ".o_input",
        content: _t("<b> Choose a name</b> for your customer / contact."),
        position: "right",
    }, {
        trigger: ".o_address_format .o_address_street ",
        content: _t("<b>Enter Your Customer / Contact Address </b>"),
        position: "top",
    }, {
        trigger: ".o_notebook .tab-content .o-kanban-button-new",
        content: _t("Click here to <b> Add Contact </b> for Your Customer "),
        position: "right",
    }, {
        trigger: ".modal-content .o_group .o_input",
        content: _t("<b>Choose a name</b> for your contact, example: <i>'Sarah'</i>"),
        position: "right",
    }, {
        trigger: ".modal-content .modal-footer .btn.btn-primary",
        content: _t("Click here to <b> Save Your Contact.</b>"),
        position: "top",
    }, {
        trigger: ".o_form_button_save",
        content: _t("Click here to <b> Save Your Customer / Contact Details.</b>"),
        position: "bottom",
    }, {
        trigger: ".breadcrumb-item:not(.active):last",
        content: _t("Use the breadcrumbs to <b>go back to your Customer / Contact list. </b> <br/><br/> Good job! You completed the tour of Customer / Contact Creation."),
        position: "bottom",
        edition: 'community',
    }]);
});
