odoo.define('pivotino_web_responsive.AppsMenu', function (require) {
    "use strict";

    var AppsMenu = require('web.AppsMenu');

    AppsMenu.include({
        init: function (parent, menuData) {
            this._super.apply(this, arguments);
            this._activeApp = undefined;
            this._apps = _.map(menuData.children, function (appMenuData) {
                return {
                    actionID: parseInt(appMenuData.action.split(',')[1]),
                    menuID: appMenuData.id,
                    name: appMenuData.name,
                    xmlID: appMenuData.xmlid,
                    web_large_icon: appMenuData.web_large_icon,
                    web_large_icon_data: appMenuData.web_large_icon_data,
                };
            });
        },
    });
});