odoo.define('pivotino_crm.relational_fields', function (require) {
    "use strict";

    var RelationFields = require('web.relational_fields');

    RelationFields.FieldStatus.include({
        // customisation starts here
        // override the _onClickStage to attach special functionality for
        // crm_lead model.
        _onClickStage: function (e) {
            var self = this;
            var sup = this._super;
            var args = arguments;
            // if the user change the stage from any stage to lost stage in
            // statusbar, then prompt lost reason wizard
            if (self.model == 'crm.lead') {
                var res_id = self.res_id;
                var new_stage_id = parseInt($(e.currentTarget).data("value"));
                // perform rpc call to get the is_lost attribute of the stage
                return self._rpc({
                    model: 'crm.stage',
                    method: 'search_read',
                    domain: [['id', '=', new_stage_id]],
                    fields: ['is_lost'],
                    limit: 1,
                }).then(function (stage){
                    // if the new stage is a lost stage, then prompt wizard
                    if (stage[0]['is_lost']) {
                        var lost_reason_action = {
                            name: 'Lost Reason',
                            type: 'ir.actions.act_window',
                            res_model: 'crm.lead.lost',
                            view_mode: 'form',
                            views: [[false, 'form']],
                            target: 'new',
                            context: {'active_ids': res_id},
                        };
                        return self.do_action(lost_reason_action).then(function (){
                            // have to perform reload after the user perform action
                            // in the wizard
                            $('.reason-apply,.reason-cancel,.close').click(function (e)
                            {
                                setTimeout(function(){
                                    self.trigger_up('reload');
                                }, 500);
                            });
                        });
                    } else {
                        sup.apply(self, args);
                    }
                });
            }
            // customisation end here
            // do normal operation
            this._super.apply(this, arguments);
        },
    });
});
