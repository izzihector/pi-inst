odoo.define('pivotino_user_guide.activity_dashboard', function(require) {
    "use strict";

    var core = require('web.core');
    var tour = require('web_tour.tour');
    var _t = core._t;

    tour.register('activity_dashboard', {
        url: "/web",
        pivotino_tour: true,
        display_name: 'Activity Dashboard',
        tour_summary: 'Tag line for this Tour',
        tour_type: 'onScreen1',
        'skip_enabled': true,
    }, [{
        edition: "community",
        trigger: ".o_main_navbar .o_menu_apps",
        content: _t('Click on the <i><b>Home icon</b></i> to navigate across apps.'),
        position: "bottom",
    }, {
        trigger: '.o_app[data-menu-xmlid="pivotino_mail.pivotino_activity_menu"]',
        content: _t("Ready to manage your activities ? your <b>all activities</b> can be found here, under the <b>Activities</b> app."),
        position: 'bottom',
        edition: 'community',
    }, {
        trigger: ".card_action_all_activity",
        content: _t("Click here to see <b> your all activities.</b> <br/> This dashboard helps you get instant view of all your business activities."),
        position: "top",
    }, {
        trigger: ".o_kanban_record:first() .btn-mark-done",
        content: _t("Click here to mark your activity as <b> Done. </b> </br></br> In this view, youc can do mark activity as <b> Done / Cancel / View Source Document </b> but you can't edit.</br></br> To edit your activity, click on <b>view document</b> > find your activity in chatter > click on edit."),
        position: "bottom",
    }, {
        trigger: ".o_input[name='feedback']",
        content: _t("Enter your<b> feedback </b> for your activity."),
        position: "right",
    }, {
        trigger: ".modal-footer .feedback-apply",
        content: _t("Click here to <b> submit your feedback.</b>"),
        position: "top",
    }, {
        trigger: ".breadcrumb-item:not(.active):last",
        content: _t("Use the breadcrumbs to <b>go back to your activities dashboard</b> <br/> Good job! You completed the tour of <b> Activity Dashboard </b>"),
        position: "bottom",
        edition: 'community',
    }]);
});
