odoo.define('pivotino_user_guide.create_meeting_in_calendar', function(require) {
    "use strict";

    var core = require('web.core');
    var tour = require('web_tour.tour');
    var _t = core._t;

    tour.register('create_meeting_in_calendar', {
        url: "/web",
        pivotino_tour: true,
        display_name: 'Create Meeting In Calendar',
        tour_summary: 'Tag line for this Tour',
        tour_type: 'onScreen0',
        'skip_enabled': true,
    }, [{
        edition: "community",
        trigger: ".o_main_navbar .o_menu_apps",
        content: _t('Click on the <i><b>Home icon</b></i> to navigate across apps.'),
        position: "bottom",
    }, {
        trigger: '.o_app[data-menu-xmlid="calendar.mail_menu_calendar"]',
        content: _t("Ready to manage your Meetings ? Your <b>all meeting </b> can be found here, under the <b>Calendar</b> app."),
        position: 'bottom',
        edition: 'community',
    }, {
        trigger: ".o_calendar_button_month",
        content: _t("Click here to <b>  view calendar by month.</b>"),
        position: "top",
    }, {
        trigger: ".o_calendar_view .fc-today .fc-day-number",
        content: _t("<b> Select a date</b> for set the meeting."),
        position: "top",
    }, {
        trigger: ".o_calendar_quick_create .o_input[name='name']",
        content: _t("<b> Click here to </b> add summary of meeting."),
        position: "top",
    }, {
        trigger: ".modal-footer .btn.btn-secondary",
        content: _t("<b> Click here to </b> edit the meeting."),
        position: "bottom",
    }, {
        trigger: ".o_field_widget[name='partner_ids']",
        content: _t("<b> Click here to </b> add new attendees for meeting."),
        position: "top",
    }, {
        trigger: ".modal-footer .btn.btn-primary",
        content: _t("<b> Click here to </b> save the meeting.<br/><br/> Congratulations, You are successfull Created New Meeting."),
        position: "top",
        edition: 'community'
    }]);
});
