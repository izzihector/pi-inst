odoo.define('pivotino_pre_config.WebClient', function (require) {
    "use strict";

    var WebClient = require('web.WebClient');
    var session = require('web.session');

    WebClient.include({
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
                                return self.menu_dp.add(self._rpc({
                                    model: 'res.users',
                                    method: 'read',
                                    args: [session.uid, ["action_id", "login_date", "first_log_bool", "clogin", "starter_view_id"]],
                                })).then(function (result) {
                                    var data = result[0];
                                    if (data.first_log_bool === false){
                                        var first_login_action = {
                                            name: 'Welcome Page',
                                            type: 'ir.actions.act_window',
                                            res_model: 'first.time.login',
                                            view_mode: 'form',
                                            views: [[false, 'form']],
                                            target: 'new',
                                        };
                                        return self.do_action(first_login_action).then(function () {
                                            $('.skip').show();
                                            $('.done').hide();
                                            $('#carouselExampleIndicators').find('.carousel-control-prev').hide();
                                            $('#carouselExampleIndicators').bind('slid.bs.carousel', function (e)
                                            {
                                                var $this = $(this);

                                                if ($this.find('.carousel-inner .carousel-item.last').hasClass('active'))
                                                {
                                                    $this.find('.carousel-control-next').hide();
                                                    $('.skip').hide();
                                                    $('.done').show();
                                                } else if ($this.find('.carousel-inner .carousel-item.first').hasClass('active'))
                                                {
                                                    $this.find('.carousel-control-prev').hide();
                                                } else {
                                                    $this.find('.carousel-control-next').show();
                                                    $this.find('.carousel-control-prev').show();
                                                }
                                            });
                                            $('.close').hide();
                                            $('.modal-header').css({"justify-content": "center",});
                                            self.menu.change_menu_section(self.menu.action_id_to_primary_menu_id(data.action_id[0]));
                                        });
                                    }
                                    else if (!data.clogin) {
                                        return self.do_action({
                                            name: 'Welcome To PIVOTINO',
                                            res_model: 'starter.wizard',
                                            views: [[data.starter_view_id || false, 'form']],
                                            type: 'ir.actions.act_window',
                                            view_mode: 'form',
                                            target: 'new'
                                        });
                                    }
                                });
                            });
                        } else {
                            self.menu.openFirstApp();
                        }
                    });
                } else {
                    return self.on_hashchange();
                }
            });
        },
    });
});
