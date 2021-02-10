odoo.define('pivotino_web_responsive.nav_footer', function (require) {
    "use strict";

    var Widget = require('web.Widget');
    var session = require('web.session');
    var core = require('web.core');
    var Menu = require('web.Menu');
    var concurrency = require('web.concurrency');
    var data_manager = require('web.data_manager');

    var _t = core._t;
    var QWeb = core.qweb;

    var NavigationFooter = Widget.extend({
        template: 'NavigationFooter',

        events: {
            'click .nav_footer_tab': '_onNavigationTab',
        },

        init: function () {
            var self = this;
            this.menu_dp = new concurrency.DropPrevious();

            this._super.apply(this, arguments);
        },

        start: function () {
            var self = this;
            this._$navButtons = this.$('.nav_button');
            this._super.apply(this, arguments);

            // load menu data for button functionality
            (odoo.loadMenusPromise || odoo.reloadMenus())
            .then(function (menuData) {
                self.menu_data = menuData;
            });

            // get current res.users obj for home action (action_id)
            this._rpc({
                model: 'res.users',
                method: 'search_read',
                domain: [['id', '=', session.uid]],
            }).then(function (user) {
                self.currentUser = user;
            });

        },

        _onNavigationTab: function (event) {
            var self = this;
            var $target = $(event.currentTarget);
            this._$navButtons.removeClass('active');
            $target.addClass('active');
            if ($target[0].id === 'dashboard') {
                // temporary go to CRM / Overview
                // FIXME: Need to fix to take care multiple dashboard in future
                for (var i = 0; i < this.menu_data.children.length; i++) {
                    if (this.menu_data.children[i].xmlid === 'crm.crm_menu_root') {
                        var dashboardMenu = this.menu_data.children[i];
                    }
                }

                // define action options
                var options = {
                    clear_breadcrumbs: true,
                    action_menu_id: dashboardMenu.id,
                };

                // do action and clear breadcrumb to avoid stacking
                self.menu_dp.add(data_manager.load_action(dashboardMenu.action.split(',')[1]))
                .then(function (result) {
                    self.do_action(result, options).then(function () {
                        core.bus.trigger('change_menu_section', dashboardMenu.id);
                    });
                });
            } else if ($target[0].id === 'lead') {
                // get CRM menu data
                var crmRoot = _.findWhere(this.menu_data.children, {xmlid: 'crm.crm_menu_root'});
                // get CRM > Pipeline menu data
                var leadRoot = _.findWhere(crmRoot.children, {xmlid: 'crm.crm_menu_sales'});
                // get CRM > Pipeline > My Pipeline menu data
                var leadMenu = _.findWhere(leadRoot.children, {xmlid: 'crm.menu_crm_opportunities'});

                // define action options
                var options = {
                    clear_breadcrumbs: true,
                    action_menu_id: leadMenu.id,
                };

                // do action and clear breadcrumb to avoid stacking
                self.menu_dp.add(data_manager.load_action(leadMenu.action.split(',')[1]))
                .then(function (result) {
                    self.do_action(result, options).then(function () {
                        core.bus.trigger('change_menu_section', crmRoot.id);
                    });
                });
            } else if ($target[0].id === 'contact') {
                // get Contacts
                var contactRoot = _.findWhere(this.menu_data.children, {xmlid: 'contacts.menu_contacts'});
                // get Contacts > Contacts
                var contactMenu = _.findWhere(contactRoot.children, {xmlid: 'contacts.res_partner_menu_contacts'});

                // define action options
                var options = {
                    clear_breadcrumbs: true,
                    action_menu_id: contactMenu.id,
                };

                // do action
                self.menu_dp.add(data_manager.load_action(contactMenu.action.split(',')[1]))
                .then(function (result) {
                    self.do_action(result, options).then(function () {
                        core.bus.trigger('change_menu_section', contactRoot.id);
                    });
                });
            } else if ($target[0].id === 'more') {
                console.log('>>>>> COMING SOON <<<<<')
            }
        },

    });

    return NavigationFooter;
});