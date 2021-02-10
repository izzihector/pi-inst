odoo.define('pivotino_web_responsive', function (require) {
    "use strict";

    var Menu = require("web.Menu");

    Menu.include({
        events: _.extend({
            // clicking home page button for hide and show
            "show.bs.dropdown .o_menu_apps": "_hideSubmenuIcon",
            "hide.bs.dropdown .o_menu_apps": "_showSubmenuIcon",
        }, Menu.prototype.events),

        // show submenu button
        _showSubmenuIcon: function () {
            this.$menu_toggle.show()
        },

        // hide submenu button
        _hideSubmenuIcon: function () {
            this.$menu_toggle.hide()
        },

    });
});