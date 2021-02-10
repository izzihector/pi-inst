# -*- coding: utf-8 -*-

from odoo import api, fields, tools, models, _
from odoo.exceptions import ValidationError, Warning, UserError, AccessError
from dateutil.relativedelta import relativedelta


class CrmLead(models.Model):
    _inherit = 'crm.lead'
    _description = "Opportunity"

    mark_lost_date = fields.Date(string='Lost Date', copy=False)
    stage_before_lost = fields.Many2one('crm.stage',
                                        string='Stage Before Lost',
                                        copy=False)
    is_lost = fields.Boolean(related='stage_id.is_lost')
    is_won = fields.Boolean(related='stage_id.is_won')
    lost_reason = fields.Many2one(copy=False)
    lost_reason_category = fields.Many2one(
        related='lost_reason.reason_category_id',
        string='Lost Reason Category',
        store=True
    )
    activity_due_date = fields.Datetime(compute='_compute_activity_due',
                                        string='Activity Due Date',
                                        store=True)
    stage_duration_ids = fields.One2many('crm.stage.duration',
                                         'lead_id',
                                         string='Stage Durations')
    duration_to_won = fields.Integer(compute='_compute_duration_to_won',
                                     string='Days To Win',
                                     store=True)
    date_deadline = fields.Date('Expected Closing',
                                help="Estimate of the date on which the "
                                     "opportunity will be won.")
    date_manual_deadline = fields.Date('Manual Expected Closing',
                                       help="Manually input estimate date won")
    lead_currency = fields.Many2one('res.currency',
                                    string='Currency',
                                    required=True,
                                    default=lambda
                                        x: x.env.company.currency_id)
    planned_revenue_input = fields.Float('Amount')
    planned_revenue = fields.Monetary('Amount',
                                      currency_field='lead_currency',
                                      tracking=True,
                                      readonly=True)
    final_revenue = fields.Float(compute='_compute_final_revenue',
                                 string='Amount',
                                 store=True)
    is_from_so = fields.Boolean(
        string='Opportunity from Sale Order',
        default=False, copy=False
    )

    # Remove Sales Team Settings
    def _notify_get_groups(self):
        res = super(CrmLead, self)._notify_get_groups()
        for group in res:
            actions = group[2].get('actions')
            if actions:
                for i in range(len(actions)):
                    if actions[i].get('title') == 'Sales Team Settings':
                        del actions[i]
        return res

    @api.depends('is_won', 'planned_revenue', 'sale_amount_total')
    def _compute_final_revenue(self):
        """ Populate the final revenue based on the stage.
        Once the quotation of the lead is confirmed, the final revenue will be
        the sum of the quotations' amount_total. Otherwise, the final revenue
        will be same as the planned_revenue.
        """
        for rec in self:
            if rec.is_won:
                rec.final_revenue = rec.sale_amount_total
            else:
                rec.final_revenue = rec.planned_revenue

    @api.depends('is_won', 'stage_duration_ids',
                 'stage_duration_ids.stage_start_date',
                 'stage_duration_ids.stage_end_date')
    def _compute_duration_to_won(self):
        """ Get the duration from creating a lead to winning the lead
        """
        for rec in self:
            rec.duration_to_won = False
            # only calculate this field when the lead is won
            if rec.is_won:
                # get all the stage_duration except the won stage
                duration_except_won = rec.stage_duration_ids.filtered(
                    lambda m: not m.stage_id.is_won)
                # sum the duration of the stages
                rec.duration_to_won = \
                    sum(duration_except_won.mapped('duration'))

    def action_sale_quotations_new(self):
        if not self.partner_id:
            self.write({
                'partner_id': self._create_partner()
            })
            self._onchange_partner_id()
            return self.action_new_quotation()
        else:
            return self.action_new_quotation()

    def _create_partner(self):
        """ Create partner based on action.
            :return int: created res.partner id
        """
        self.ensure_one()
        result = self.handle_partner_assignation(action='create')
        return result.get(self.id)

    @api.model
    def _auto_mark_lost_lead(self):
        """ This method is called from a cron job.
        It is used to mark leads as lost when the lead meets its date_deadline.
        """
        # get all the leads which are expired and not in (Won and Lost) stage
        records = self.search([
            ('stage_id.is_won', '=', False),
            ('stage_id.is_lost', '=', False),
            ('date_deadline', '<=', fields.Date.today())
        ])
        # set the lost reason as 'poor follow up time'
        default_lost_reason = self.env.ref('pivotino_crm.lost_reason_8')
        # mark leads as lost
        for rec in records:
            rec.with_context(from_cron=True).\
                action_set_lost(lost_reason=default_lost_reason.id)

    def action_set_lost(self, **additional_values):
        """ Have to override the function otherwise there will be 2 records in
        chatter log. Write the current stage to stage_before_lost, and the
        lost time. Don't archive the lead when it goes to lost.
        Lost semantic: probability = 0 or active = False """
        lost_stage = self.env.ref('pivotino_crm.stage_lead6')
        # get the current stage
        current_stage = self.stage_id
        # write the current stage to field stage_before_lost
        result = self.write({'probability': 0,
                             'automated_probability': 0,
                             'stage_id': lost_stage.id,
                             'stage_before_lost': current_stage,
                             'mark_lost_date': fields.Date.today(),
                             'date_deadline': fields.Date.today(),
                             **additional_values})
        self.write({
            'date_closed': fields.Datetime.now(),
        })
        # cancel the linked quotations if a lead is marked as lost
        quotations = [order for lead in self for order in lead.order_ids
                      if order.state not in ['done', 'cancel', 'sale']]
        if quotations:
            for quotation in quotations:
                quotation.with_context(from_lost_reason=True).action_cancel()
        self._rebuild_pls_frequency_table_threshold()
        return result

    @api.depends('activity_ids', 'activity_ids.date_deadline')
    def _compute_activity_due(self):
        """ Get the earliest deadline of activities
        """
        for rec in self:
            # by default, due date should be False
            rec.activity_due_date = False
            if rec.activity_ids:
                # sort the activities using deadline asc
                activities = rec.activity_ids.sorted(
                    key=lambda r: r.date_deadline)
                # change the due date to the earliest deadline
                if activities[0]:
                    rec.activity_due_date = activities[0].date_deadline

    @api.model
    def create(self, values):
        res = super(CrmLead, self).create(values)
        res.planned_revenue = res.planned_revenue_input * \
                              self.env['res.currency']._get_conversion_rate(
                                  res.lead_currency,
                                  res.company_currency,
                                  res.env.company,
                                  fields.Date.today())
        # create lead stage duration
        # change the logic here because a lead might be created from a manual
        # quotation, so the first stage of the lead should not be 'New' anymore
        # but 'Quotation'.
        if 'stage_id' in values:
            current_stage = self.env['crm.stage'].search(
                [('id', '=', values.get('stage_id'))])
        else:
            current_stage = self.env['crm.stage'].search(
                [], order='stage_sequence', limit=1)
        lead_stage_duration_obj = self.env['crm.stage.duration']
        lead_stage_duration_obj.create({
            'lead_id': res.id,
            'stage_id': current_stage.id,
            'stage_start_date': fields.Datetime.now(),
        })
        # if the lead is created in Quotation Stage, then create to_do activity
        # instead of first activity
        if res.stage_id.is_quotation:
            todo_activity_vals = self._get_todo_activity(res)
            self.env['mail.activity'].create(todo_activity_vals)
        else:
            first_activity_vals = self._get_first_activity(res)
            self.env['mail.activity'].create(first_activity_vals)

        # update analytic tracking opportunity count
        opportunity_count_rec = self.env.ref(
            'pivotino_crm.analytic_opportunity_count')
        opportunity_count_rec.tracking_record_increment_integer(1)
        return res

    def write(self, values):
        # mark activity as done when change stage from new to first activity
        first_activity_stage = self.env.ref('crm.stage_lead2')
        won_stage = self.env.ref('pivotino_crm.stage_lead5').id
        lost_stage = self.env.ref('pivotino_crm.stage_lead6').id
        todo_activity = self.env.ref('mail.mail_activity_data_todo')
        activity_type = self.env.ref(
            'pivotino_crm.mail_activity_first_activity')
        stage_id = values.get('stage_id')

        for rec in self:
            if values.get('date_deadline') and not self.env.context.get(
                    'from_activity'):
                rec.date_manual_deadline = values.get('date_deadline')

            if values.get('planned_revenue_input') and values.get('lead_currency'):
                currency = self.env['res.currency'].search(
                    [('id', '=', values.get('lead_currency'))])
                rec.planned_revenue = values.get('planned_revenue_input') * \
                                      self.env['res.currency']._get_conversion_rate(
                                          currency,
                                          self.company_currency,
                                          self.env.company,
                                          fields.Date.today())
            elif values.get('planned_revenue_input'):
                rec.planned_revenue = values.get('planned_revenue_input') * \
                                      self.env['res.currency']._get_conversion_rate(
                                          rec.lead_currency,
                                          self.company_currency,
                                          self.env.company,
                                          fields.Date.today())
            elif values.get('lead_currency'):
                currency = self.env['res.currency']\
                    .search([('id', '=', values.get('lead_currency'))])
                rec.planned_revenue = rec.planned_revenue_input * \
                                      self.env['res.currency']._get_conversion_rate(
                                          currency,
                                          self.company_currency,
                                          self.env.company,
                                          fields.Date.today())

            if stage_id:
                now = fields.Datetime.now()
                # get the old stage duration record and update stage_end_date
                old_stage_duration = rec.stage_duration_ids.filtered(
                    lambda m: m.stage_id.id == rec.stage_id.id)
                old_stage_duration.stage_end_date = now
                new_stage = self.env['crm.stage'].browse(
                    values.get('stage_id'))
                stage_end_date = False
                # if the new stage is won or lost, then set end date as today
                if new_stage.is_won or new_stage.is_lost:
                    stage_end_date = now
                # create the new stage duration record and set stage_start_date
                self.env['crm.stage.duration'].create({
                    'lead_id': rec.id,
                    'stage_id': values.get('stage_id'),
                    'stage_start_date': now,
                    'stage_end_date': stage_end_date,
                })

                for activity in rec.activity_ids:
                    if activity.activity_type_id == activity_type:
                        if not self.env.context.get('action_done'):
                            activity.with_context(from_lead=True)\
                                ._action_done()
                    elif activity.activity_type_id == todo_activity:
                        if not self.env.context.get('action_done'):
                            activity.with_context(
                                from_lead=True)._action_done()

                # raise warning if there are pending activities in a won or
                # lost lead. Do not raise warning if the lead is closed by
                # cron job.
                if (new_stage.is_won or new_stage.is_lost) and \
                        rec.activity_ids and \
                        not self.env.context.get('from_cron'):
                    raise UserError(_('There are still activities pending '
                                      'for this opportunity. Please mark '
                                      'them as done / cancel them before '
                                      'closing this opportunity.'))

                if not rec.activity_ids:
                    if stage_id not in (won_stage, lost_stage):
                        activity_vals = rec._get_todo_activity(rec)
                        self.env['mail.activity'].create(activity_vals)

                stage = self.env['crm.stage'].search([('id', '=', stage_id)])
                if rec.is_lost:
                    if stage.stage_sequence < rec.stage_id.stage_sequence:
                        if rec.date_deadline and rec.date_deadline < fields.Date.today():
                            raise Warning(_('In order to move the opportunity from LOST, '
                                            'please amend the Expected Closing date to a '
                                            'future date before proceeding. '))
        res = super(CrmLead, self).write(values)
        # change the salesperson of the child quotations including SO.
        # change the customer of the child quotations including SO.
        for rec in self:
            if 'user_id' in values:
                for order in rec.order_ids:
                    order.user_id = values.get('user_id')

            if values.get('partner_id'):
                for order in rec.order_ids:
                    order.partner_id = values.get('partner_id')
        return res

    def _get_todo_activity(self, res_id):
        activity_type = self.env.ref('mail.mail_activity_data_todo')
        base = fields.Date.context_today(self)
        date_deadline = base + relativedelta(
            **{activity_type.delay_unit: activity_type.delay_count})
        summary = 'Follow Up'
        user = activity_type.default_user_id or self.env.user
        note = 'System has helped you to schedule this activity. ' \
               'Please continue to follow up on this opportunity.'
        res_model = self.env['ir.model']._get(self._name).id

        return {
            'summary': summary,
            'activity_type_id': activity_type.id,
            'res_model_id': res_model,
            'res_id': res_id.id,
            'date_deadline': date_deadline,
            'user_id': user.id,
            'note': note
        }

    def _get_first_activity(self, res_id):
        activity_type = self.env.ref(
            'pivotino_crm.mail_activity_first_activity')
        base = fields.Date.context_today(self)
        date_deadline = base + relativedelta(
            **{activity_type.delay_unit: activity_type.delay_count})
        summary = 'First Activity created by System'
        user = activity_type.default_user_id or self.env.user
        note = 'System has helped you to set up this activity. ' \
               'Please contact your opportunity to start the First Activity.'
        res_model = self.env['ir.model']._get(self._name).id

        return {
            'summary': summary,
            'activity_type_id': activity_type.id,
            'res_model_id': res_model,
            'res_id': res_id.id,
            'date_deadline': date_deadline,
            'user_id': user.id,
            'note': note
        }

    def _generate_order_by(self, order_spec, query):
        """
        Attempt to construct an appropriate ORDER BY clause based on crm lead sequence configured by user.
        Overwrote from base.
        """
        order_by_clause = ''
        leads = self.get_order_by_field()
        order_spec = order_spec or leads
        if order_spec:
            order_by_elements = self._generate_order_by_inner(self._table, order_spec, query)
            if order_by_elements:
                order_by_clause = ",".join(order_by_elements)

        return order_by_clause and (' ORDER BY %s ' % order_by_clause) or ''

    def get_order_by_field(self):
        """
        Get the order of sequence
        """
        lead_name = ''
        lead_sequences = self.env['crm.lead.sequence'].search([('include_sequence', '!=', False)])
        if lead_sequences:
            lead_sequences = sorted(lead_sequences, key=lambda item: item.lead_sequence)

        if lead_sequences:
            lead_name = ', '.join([x.field_id.name + ' ' + x.asc_desc for x in lead_sequences])

        return lead_name

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None,
                   orderby=False, lazy=True):
        # Need to ask Jocelyn/Nicole whether do we need this since we can apply
        # filter + groupby to achieve similar result
        if 'lost_reason' in groupby:
            domain.insert(0, ['lost_reason', '!=', False])
        if 'lost_reason_category' in groupby:
            domain.insert(0, ['lost_reason_category', '!=', False])
        res = super(CrmLead, self).read_group(domain, fields, groupby, offset,
                                              limit, orderby, lazy)
        return res

    def _onchange_compute_probability(self, optional_field_name=None):
        # Overwrote from base to remove naive bayes algorithm and use our own
        if optional_field_name and optional_field_name not in self._pls_get_safe_fields():
            return
        lead_probabilities = self._pls_get_naive_bayes_probabilities()
        self.automated_probability = lead_probabilities.get(self.id, 0)
        self._update_probability()


    def _update_probability(self):
        # Overwrote from base to remove naive bayes algorithm and use our own
        if self.stage_id == self.env.ref('crm.stage_lead1'):
            if self.probability < 10.00:
                self.probability = 10.00
        elif self.stage_id == self.env.ref('crm.stage_lead2'):
            if self.probability < 25.00:
                self.probability = 25.00
        elif self.stage_id == self.env.ref('crm.stage_lead3'):
            if self.probability < 50.00:
                self.probability = 50.00
        elif self.stage_id == self.env.ref('crm.stage_lead4'):
            if self.probability < 80.00:
                self.probability = 80.00
        elif self.stage_id == self.env.ref('pivotino_crm.stage_lead5'):
            if self.probability < 100.00:
                self.probability = 100.00
        else:
            self.probability = 0.00
        return True

    def _cron_update_automated_probabilities(self):
        # Clear the frequencies table (in sql to speed up the cron)
        # Overwrote from base to avoid using naive abyes algorithm and use our own
        try:
            self.check_access_rights('unlink')
        except AccessError:
            raise UserError(_("You don't have the access needed to run this cron."))
        else:
            self._cr.execute('TRUNCATE TABLE crm_lead_scoring_frequency')

        pls_start_date = self._pls_get_safe_start_date()
        if pls_start_date:
            pending_lead_domain = ['&', '&', ('stage_id', '!=', False),
                                   ('create_date', '>', pls_start_date),
                                   '|', ('probability', '=', False), '&',
                                   ('probability', '<', 100),
                                   ('probability', '>', 0)]
            leads_to_update = self.env['crm.lead'].search(pending_lead_domain)

            for lead in leads_to_update:
                lead._update_probability()

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        """ Inherit this function due to not showing all stages in chart
        when there is no record in the stage
        """
        context = self.env.context
        from_dashboard = context.get('from_dashboard')
        if from_dashboard:
            return stages
        return super(CrmLead, self)._read_group_stage_ids(stages, domain, order)

    @api.model
    def get_import_templates(self):
        return [{
            'label': _('Import Template for Leads & Opportunities'),
            'template': '/pivotino_crm/static/xls/crm_lead.xls'
        }]


class LeadSequence(models.Model):
    _name = "crm.lead.sequence"
    _description = 'Determine the sequence of lead'

    name = fields.Char(string='Name')
    include_sequence = fields.Boolean(string="Include in lead sequence?")
    lead_sequence = fields.Integer(string='Lead Sequence', default=0)
    field_id = fields.Many2one('ir.model.fields', string='Lead Fields',
                               domain="[('model_id', '=', 'crm.lead')]")
    asc_desc = fields.Selection([('asc', 'asc'), ('desc', 'desc')],
                                string='Ascending / Descending',
                                required=True)

    @api.constrains('lead_sequence', 'field_id')
    def _check_duplicate(self):
        lead_sequence = self.search([
            '|',
            ('lead_sequence', '=', self.lead_sequence),
            ('field_id', '=', self.field_id.id),
            ('id', '!=', self.id)
        ])
        if self.lead_sequence and lead_sequence:
            raise ValidationError(_('This sequence is selected in another '
                                    'Lead Sequence Configuration!'))

    @api.model
    def create(self, values):
        res = super(LeadSequence, self).create(values)
        if res.lead_sequence == 0:
            res.update_sequence()
        return res

    def update_sequence(self):
        mylist = []
        for lead in self.search([]):
            mylist.append(lead.lead_sequence)
        self.lead_sequence = max(mylist) + 1
