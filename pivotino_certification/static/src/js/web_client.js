odoo.define('pivotino_certification.WebClient', function (require) {
    'use strict';

    var WebClient = require('web.WebClient');
    var session = require('web.session');
    var core = require('web.core');
    var data_manager = require('web.data_manager');
    var Sidebar = require('web.Sidebar');

    var _t = core._t;

    Sidebar.include({
        _addItems: function(section_code, items){
            var self = this;
            var _super = this._super;
            var export_label = _t("Export");
            var new_items = items;
            if (section_code === "other") {
                new_items = [];
                for (var i = 0; i < items.length; i++) {
                    if (items[i]["label"] !== export_label) {
                        new_items.push(items[i]);
                    }
                }
            }
            if (new_items.length > 0) {
                _super.call(self, section_code, new_items);
            }
        }
    });

    WebClient.include({
        /*
        * change the login mechanism for certification
        */
        show_application: function () {
            var self = this;
            this.set_title();

            return this.menu_dp.add(this.instanciate_menu_widgets()).then(function () {
                $(window).bind('hashchange', self.on_hashchange);

                // If the url's state is empty, we execute the user's home action if there is one (we
                // show the first app if not)
                var state = $.bbq.getState(true);
                if (_.keys(state).length === 1 && _.keys(state)[0] === "cids") {
                    return self.menu_dp.add(self._rpc({
                            model: 'res.users',
                            method: 'read',
                            args: [session.uid, ["action_id"]],
                        }))
                        .then(function (result) {
                            var data = result[0];
                            if (data.action_id) {
                                return self.do_action(data.action_id[0]).then(function () {
                                    self.menu.change_menu_section(self.menu.action_id_to_primary_menu_id(data.action_id[0]));
                                });
                            } else {
                                // self.menu.openFirstApp();
                                // open lead crm kanban instead of first app
                                // get menu id of CRM for changing menu section
                                for (var i = 0; i < self.menu.menu_data.children.length; i++) {
                                    if (self.menu.menu_data.children[i].xmlid === 'crm.crm_menu_root') {
                                        var crmMenu = self.menu.menu_data.children[i]
                                    }
                                }
                                // define action options
                                var options = {
                                    clear_breadcrumbs: true,
                                    action_menu_id: crmMenu.id,
                                };
                                // do action and clear breadcrumb to avoid stacking
                                self.menu_dp.add(data_manager.load_action(crmMenu.action.split(',')[1]))
                                .then(function (result) {
                                    self._openMenu(result, options).then(function () {
                                        core.bus.trigger('change_menu_section', crmMenu.id);
                                    });
                                });
                            }
                        });
                } else {
                    return self.on_hashchange();
                }
            });
        },
    });
});