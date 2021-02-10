odoo.define('pivotino_mail.KanbanController', function (require) {
    "use strict";

    var KanbanController = require('web.KanbanController');

    KanbanController.include({

        _onButtonClicked: function (ev) {
            var self = this;
            ev.stopPropagation();
            var attrs = ev.data.attrs;
            var record = ev.data.record;
            // if the user mark activity as done in kanban, then prompt wizard
            // and ask for feedback. if the user cancel activity, directly
            // unlink the record.
            if ('context' in attrs){
                if (attrs.context.includes('mark_activity_as_done')){
                    var res_id = record.data.id;
                    var lost_reason_action = {
                        name: 'Activity Feedback',
                        type: 'ir.actions.act_window',
                        res_model: 'mail.feedback',
                        view_mode: 'form',
                        views: [[false, 'form']],
                        target: 'new',
                        context: {'active_ids': res_id},
                    };
                    return self.do_action(lost_reason_action).then(function (){
                        // have to perform reload after the user perform action
                        // in the wizard
                        $('.feedback-apply').click(function (e)
                        {
                            setTimeout(function(){
                                self.trigger_up('reload');
                            }, 500);
                        });
                    });
                } else if (attrs.context.includes('cancel_activity')){
                    var res_id = record.data.id;
                    return this._rpc({
                        model: 'mail.activity',
                        method: 'unlink',
                        args: [res_id],
                    }).then(function (){
                        setTimeout(function(){
                            self.trigger_up('reload');
                        }, 500);
                    });
                } else if (attrs.context.includes('view_source_document')){
                    var view_document_action = {
                        name: record.data.res_name,
                        res_model: record.data.res_model,
                        type: 'ir.actions.act_window',
                        view_mode: 'form',
                        views: [[false, 'form']],
                        target: 'current',
                        res_id: record.data.res_id,
                    }
                    return self.do_action(view_document_action);
                }
            }
            else {
                this._super.apply(this, arguments);
            }
        },
    });
});
