odoo.define('pivotino_user_guide.change_password', function(require) {
    "use strict";

    var core = require('web.core');
    var tour = require('web_tour.tour');
    var _t = core._t;

    tour.register('change_password', {
        url: "/web",
        pivotino_tour: true,
        display_name: 'Change Password (Business Owner Only)',
        tour_summary: 'Tag line for this Tour',
        tour_type: 'onScreen0',
        'skip_enabled': true,
    }, [{
        edition: "community",
        trigger: ".o_main_navbar .o_menu_apps",
        content: _t('Click on the <i><b>Home icon</b></i> to navigate across apps.'),
        position: "bottom",
    }, {
        trigger: '.o_app[data-menu-xmlid="pivotino_base.menu_user_company_root"]',
        content: _t("Ready to <b> Change Password </b> for user? Your <b>all users </b> can be found here, under the <b>Configuration</b> app."),
        position: 'bottom',
        edition: 'community',
    }, {
        trigger: "tr.o_data_row td.o_data_cell:first()",
        content: _t("Click on the user to <b> Change Password.</b> <br/> Choose on the user to change their login password."),
        position: "bottom",
    }, {
        trigger: ".o_dropdown_toggler_btn .d-inline",
        content: _t("Click here to <b> open change password menu.</b>"),
        position: "top",
    }, {
        trigger: ".dropdown-menu .dropdown-item:contains(Change Password)",
        content: _t("Click here to <b>Change Password.</b>"),
        position: "right",
    }, {
        trigger: ".o_field_char[name='new_password']",
        content: _t("<b> Enter New Password</b>"),
        position: "left",
    }, {
        trigger: ".modal-footer .btn.btn-primary",
        content: _t("Clcik here to save your <b> New Password.</b>"),
        position: "top",
        edition: 'community'

    }]);
});
