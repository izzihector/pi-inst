odoo.define('pivotino_user_guide.systray', function (require) {
    "use strict";
    var config = require('web.config');
    var core = require('web.core');
    var SystrayMenu = require('web.SystrayMenu');
    var Widget = require('web.Widget');
    var tour = require('web_tour.tour');
    var TourManager = require('web_tour.TourManager');
    var local_storage = require('web.local_storage');
    var rpc = require('web.rpc');
    var Dialog = require('web.Dialog');

    var QWeb = core.qweb;
    var _t = core._t;

    var ActionMenu = Widget.extend({
        template: 'pivotino_user_guide.pivotino_help_icon',
        events: {
            'show.bs.dropdown': '_onShowDropdown',
            'click .o_filter_button': '_onClickFilterButton',
            'click .topic_help': '_onClickTopicHelp',
            'click .pivotino-user-guide-icon': '_onClickHelpButton',
            'click .topic_help[data-tour-type="onScreen2"]': '_onClickDocumentationLink',
            'click .topic_help[data-tour-type="onScreen3"]': '_onClickVideoLink',
        },

        start: function (parent) {
            var self = this;
            this._$filterButtons = this.$('.o_filter_button');
            this._$topics = this.$('.o_mail_systray_dropdown_items');

            setTimeout(function() {
                var pivotino_tour = local_storage.getItem('pivotino_tour');
                if (pivotino_tour) {
                    local_storage.removeItem('pivotino_tour');
                    self._renderTopicTour(pivotino_tour);
                }
            }, 350);
            return this._super.apply(this, arguments);
        },

        /**
         * States whether the widget is in mobile mode or not.
         * This is used by the template.
         *
         * @returns {boolean}
         */
        isMobile: function () {
            return config.device.isMobile;
        },

        /**
         * @private
         * @returns {Promise<Object[]>} resolved with list of topics marked as Pivotino Tour
         */
        _getTopics: function () {
            var allTopics = [];
            var filter;
            if (this._filter) {
                filter = this._filter;
            } else {
                if (config.device.isMobile) {
                    filter = 'onScreen2';
                } else {
                    filter = 'onScreen0';
                }
            }

            _.each(tour.tours, function (val, key) {
                if (val.pivotino_tour && val.tour_type === filter) {
                    allTopics.push(tour.tours[key]);
                }
            });

            var doneTopics = [];
            var def = rpc.query({
                model: 'web_tour.tour',
                method: 'get_consumed_tours',
            });
            doneTopics.push(def);
            return Promise.all([allTopics, doneTopics]);
        },

        /**
         * Render the list of help topics
         *
         * @private
         * @param {Object} topics list
         */
        _renderTopics: function (AllTopics) {
            var self = this;
            return Promise.all(AllTopics[1]).then(function(doneTopics) {
                _.each(AllTopics[0], function(topic) {
                    _.each(doneTopics[0], function (doneTopic) {
                        if(topic['name'] === doneTopic) {
                            topic['tour_taken'] = 1;
                        }
                    });
                });
                self._$topics.html(QWeb.render('pivotino_user_guide.pivotino_help_icon.Topics', {
                    topics: AllTopics[0],
                }));
            });
        },

        /**
         * @private
         */
        _updateTopics: function () {
            this._getTopics().then(this._renderTopics.bind(this));
        },

        /**
         * @private
         */
        _onShowDropdown: function () {
            this._updateTopics();
        },

        /**
         * @private
         * @param {MouseEvent} ev
         */
        _onClickFilterButton: function (ev) {
            ev.stopPropagation();
            this._$filterButtons.removeClass('active');
            var $target = $(ev.currentTarget);
            $target.addClass('active');
            this._filter = $target.data('filter');
            this._updateTopics();
        },

        /**
         * @private
         */
        _onClickTopicHelp: function (ev) {
            ev.preventDefault();
            var name = $(ev.target).closest('.topic_help').data('topic-name');
            var display_name = $(ev.target).closest('.topic_help').data('topic-display-name');
            var url = $(ev.target).closest('.topic_help').data('topic-url');
            var type = $(ev.target).closest('.topic_help').data('tour-type');
            if (type === 'onScreen0' || type === 'onScreen1') {
                local_storage.setItem('pivotino_tour', name);
                window.location.href = window.location.origin + url;
            }
            if (type === 'onScreen2' && url) {
                this._renderTopicLink(url);
            }
            if (type === 'onScreen3' && (url && display_name)) {
                this._renderTopicVideo(display_name, url);
            }
        },

        _onClickHelpButton: function (ev) {
            rpc.query({
                model: 'analytic.tracking',
                method: 'tracking_record_increment_help_button',
                args: [],
            });
        },

        _onClickDocumentationLink: function (ev) {
            rpc.query({
                model: 'analytic.tracking',
                method: 'tracking_record_increment_documentation',
                args: [],
            });
        },

        _onClickVideoLink: function (ev) {
            rpc.query({
                model: 'analytic.tracking',
                method: 'tracking_record_increment_video',
                args: [],
            });
        },

        /**
         * @private
         * @param {string} name
         */
        _renderTopicTour: function (name) {
            TourManager.prototype._to_next_step.call(tour, name, 0);
        },

        /**
         * @private
         * @param {string} name
         * @param {string} url
         */
        _renderTopicVideo: function (name, url) {
            var dialog = new Dialog(this, {
                size: 'large',
                title: _t(name),
                $content: $(QWeb.render("pivotino_user_guide.TopicsVideo")),
                buttons: [
                    {
                        text: _t("Close"),
                        close: true,
                    },
                ],
            });
            dialog.opened().then(function () {
                dialog.$('#video-preview').find('iframe').attr('src', url);
            });
            dialog.open();
        },

        /**
         * @private
         * @param {string} url
         */
        _renderTopicLink: function (url) {
            window.open(url, '_blank');
        },
    });

    SystrayMenu.Items.push(ActionMenu);
    return ActionMenu;
});
