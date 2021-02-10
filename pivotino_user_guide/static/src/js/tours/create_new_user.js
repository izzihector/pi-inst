odoo.define('pivotino_user_guide.create_new_user', function(require) {
    "use strict";

    var core = require('web.core');
    var tour = require('web_tour.tour');
    var _t = core._t;

    tour.register('create_new_user', {
        url: "/web",
        pivotino_tour: true,
        display_name: 'Create New User (Business Owner Only)',
        tour_summary: 'Tag line for this Tour',
        tour_type: 'onScreen1',
        'skip_enabled': true,
    }, [{
        edition: "community",
        trigger: ".o_main_navbar .o_menu_apps",
        content: _t('Click on the <i><b>Home icon</b></i> to navigate across apps.'),
        position: "bottom",
    }, {
        trigger: '.o_app[data-menu-xmlid="pivotino_base.menu_user_company_root"]',
        content: _t("Ready to manage your all users? Your <b>all users </b> can be found here, under the <b>Configuration</b> app."),
        position: 'bottom',
        edition: 'community',
    }, {
        trigger: "a[data-menu-xmlid='pivotino_base.menu_res_users']",
        content: _t("Click here to <b> open users </b> menu."),
        position: "bottom",
    }, {
        trigger: ".o_list_button_add",
        content: _t("Click here to <b> create new user.</b>"),
        position: "bottom",
    }, {
        trigger: ".o_field_char[name='name']",
        content: _t("<b> Choose a name</b> for user, example: <i>'Sarah'</i>"),
        position: "right",
    }, {
        trigger: ".o_field_char[name='login']",
        content: _t("<b> Click here to</b> enter email for login, example: <i>'admin@pivotino.com'</i>"),
        position: "right",
    }, {
        trigger: ".o_input[name='user_role']",
        content: _t("Select a <b> roll of user.</b>"),
        position: "right",
    }, {
        trigger: ".o_form_button_save",
        content: _t("Click here to <b> save your product.</b> <br/> Congratulations, You are successfull Created New User."),
        position: "bottom",
        edition: 'community'
    }]);
});
