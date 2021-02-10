odoo.define('pivotino_web_responsive.WebClient', function (require) {
    "use strict";

    var WebClient = require('web.WebClient');
    var NavigationFooter = require('pivotino_web_responsive.nav_footer');
    var config = require('web.config');
    var core = require('web.core');
    var Sidebar = require('web.Sidebar');

    var _t = core._t;

    WebClient.include({
        /*
        * Add menu data in start function
        */
        start: function () {
            (odoo.loadMenusPromise || odoo.reloadMenus())
            .then(function (menuData) {
                self.menu_data = menuData;
            });

            return this._super.apply(this, arguments);
        },
        /*
        * Add in footer for web client
        */
        instanciate_menu_widgets: function () {
            var self = this;
            var proms = [];

            return this._super.apply(this, arguments).then(function() {
                if (self.nav_footer) {
                    self.nav_footer.destroy();
                }
                self.nav_footer = new NavigationFooter(self);
                proms.push(self.nav_footer.appendTo(self.$el));
                return Promise.all(proms);
            });
        },
        /*
        * Inherit and hide the submenu icon if there is no children menu
        */
        _on_app_clicked_done: function (ev) {
            var btn_toggle = $('.o-menu-toggle');
            var curMenu = _.findWhere(this.menu_data.children, {id: ev.data.menu_id});
            if (curMenu.children.length === 0) {
                btn_toggle.hide();
            } else {
                btn_toggle.show();
            }
            return this._super.apply(this, arguments);
        },
    });

    Sidebar.include({
        /*
        * do not push export label for mobile
        */
        _addItems: function(section_code, items){
            var self = this;
            var _super = this._super;
            var export_label = _t("Export");
            var new_items = items;
            if (section_code === "other") {
                new_items = [];
                for (var i = 0; i < items.length; i++) {
                    if (items[i]["label"] === export_label) {
                        if (config.device.size_class >= config.device.SIZES.LG) {
                            new_items.push(items[i]);
                        }
                    } else {
                        new_items.push(items[i]);
                    }
                }
            }
            if (new_items.length > 0) {
                _super.call(self, section_code, new_items);
            }
        },
    });
});