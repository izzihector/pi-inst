odoo.define('pivotino_crm.KanbanModel', function (require) {
    "use strict";

    var KanbanModel = require('web.KanbanModel');
    var RelationFields = require('web.relational_fields');

    KanbanModel.include({
        // override the moveRecord to attach special functionality for
        // crm_lead model.
        moveRecord: function (recordID, groupID, parentID) {
            var self = this;
            var parent = this.localData[parentID];
            var new_group = this.localData[groupID];
            var changes = {};
            var groupedFieldName = parent.groupedBy[0];
            var groupedField = parent.fields[groupedFieldName];
            if (groupedField.type === 'many2one') {
                changes[groupedFieldName] = {
                    id: new_group.res_id,
                    display_name: new_group.value,
                };
            } else if (groupedField.type === 'selection') {
                var value = _.findWhere(groupedField.selection, {1: new_group.value});
                changes[groupedFieldName] = value && value[0] || false;
            } else {
                changes[groupedFieldName] = new_group.value;
            }

            // Manually updates groups data. Note: this is done before the actual
            // save as it might need to perform a read group in some cases so those
            // updated data might be overridden again.
            var record = self.localData[recordID];
            var resID = record.res_id;
            // Remove record from its current group
            var old_group;
            for (var i = 0; i < parent.data.length; i++) {
                old_group = self.localData[parent.data[i]];
                var index = _.indexOf(old_group.data, recordID);
                if (index >= 0) {
                    old_group.data.splice(index, 1);
                    old_group.count--;
                    old_group.res_ids = _.without(old_group.res_ids, resID);
                    self._updateParentResIDs(old_group);
                    break;
                }
            }
            // Add record to its new group
            new_group.data.push(recordID);
            new_group.res_ids.push(resID);
            new_group.count++;

            // customisation starts here
            var record_data = self.localData[recordID];
            // if the user change the stage from any stage to lost stage in
            // kanban view, then prompt lost reason wizard
            if (record_data.model == 'crm.lead' && 'stage_id' in changes) {
                var res_id = record_data.data.id;
                var new_stage_name = changes['stage_id']['display_name'];
                var new_stage_id = changes['stage_id']['id'];
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
                        // do as normal
                        return self.notifyChanges(recordID, changes).then(function () {
                            return self.save(recordID);
                        }).then(function () {
                            record.parentID = new_group.id;
                            return [old_group.id, new_group.id];
                        });
                    }
                });
            }
            // otherwise, do normal operation
            return this.notifyChanges(recordID, changes).then(function () {
                return self.save(recordID);
            }).then(function () {
                record.parentID = new_group.id;
                return [old_group.id, new_group.id];
            });
            // customisation end here
        },
    });
});
