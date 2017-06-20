# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons.budget_utilities.models.utilities import choices_tuple


class BudgetInheritOperation(models.Model):
    _inherit = 'budget.core.budget'

    # CHOICES
    # ----------------------------------------------------------

    # BASIC FIELDS
    # ----------------------------------------------------------
    is_operation = fields.Boolean(string='Is Operation')

    cost_center_account_code = fields.Char(string="CC-AC")

    # initial_expenditure_amount exist in budget.core.budget already

    # RELATIONSHIPS
    # ----------------------------------------------------------
    # company_currency_id exist in budget.core.budget already
    # history_ids exist in budget.core.budget already
    # section_id exist in budget.core.budget already so we need to overwrite here
    # budget model must be first to be import then budget_inherit_operation

    cost_center_id = fields.Many2one('budget.core.cost.center', string='Cost Center')
    account_code_id = fields.Many2one('budget.core.account.code', string='Account Code')

    # RELATED FIELDS
    # ----------------------------------------------------------
    # company_currency_id exist in budget.core.budget already
    # history_ids exist in budget.core.budget already
    cost_center_description = fields.Text(related='cost_center_id.description',
                                          string='Cost Center Description',
                                          store=True)
    account_code_description = fields.Text(related='account_code_id.description',
                                           string='Account Code Description',
                                           store=True)
    # This is Section ID Related for operation not CWP
    area_of_spend_ll_id = fields.Many2one(related='account_code_id.area_of_spend_ll_id',
                                          store=True)
    area_of_spend_hl_id = fields.Many2one(related='account_code_id.area_of_spend_hl_id',
                                          store=True)
    grouping = fields.Selection(related='account_code_id.grouping',
                                store=True)

    # COMPUTE FIELDS
    # ----------------------------------------------------------
    # company_currency_id exist in budget.core.budget
    accrued_amount = fields.Monetary(compute='_compute_accrued_amount',
                                     currency_field='company_currency_id',
                                     string='Accrued Amount',
                                     store=True)

    @api.one
    @api.depends('accrual_ids', 'accrual_ids.accrued_amount')
    def _compute_accrued_amount(self):
        # accrual_ids
        # inheriting
        if self.is_operation:
            self.accrued_amount = sum(self.accrual_ids.filtered(lambda r: r.state == 'approved').mapped('accrued_amount'))

    # TODO ENCHANCE TO REFLECT COST CENTER FROM MIXIN
    @api.onchange('cost_center_id')
    def onchange_section_id(self):
        # this exist in the main budget.py
        # inheriting
        if self.is_operation:
            self.section_id = self.cost_center_id.section_id
            self.sub_section_id = self.cost_center_id.sub_section_id

    # ONCHANGES
    # ----------------------------------------------------------
    # region_id exist in budget.core.budget
    @api.onchange('cost_center_account_code', 'cost_center_id', 'account_code_id')
    def onchange_cost_center_account_code(self):
        if self.is_operation:
            cost_center = self.cost_center_id.cost_center
            account_code = self.account_code_id.account_code

            string_list = [i for i in [cost_center, account_code] if i is not False]

            self.cost_center_account_code = '-'.join(string_list)

    # CONSTRAINS
    # ----------------------------------------------------------
    _sql_constraints = [
        ('uniq_cost_center', 'UNIQUE (cost_center_account_code)', 'Cost Center')
    ]

    # OVERRIDE METHODS
    # ----------------------------------------------------------
    @api.model
    @api.returns('self', lambda rec: rec.id)
    def create(self, values):
        if values.get('is_operation', False):
            initial_expenditure_amount = values.get('initial_expenditure_amount', 0.00)
            start_date = values.get('start_date', False)
            cost_center_account_code = values.get('cost_center_account_code', '')
            # create Initial history
            history = {
                # name exist in budget.core.budget
                'name': 'INITIAL: %s' % cost_center_account_code,
                'remarks': 'initial amount',
                'expenditure_amount': initial_expenditure_amount,
                'action_taken': 'add',
                'change_date': start_date,
                'is_initial': True,
                'is_operation_history': True
            }

            values.update(history_ids=[(0, 0, history)])

            # Equate Project No to Name
            cost_center_account_code = values.get('cost_center_account_code', '')
            values.update(name=cost_center_account_code)

        return super(BudgetInheritOperation, self).create(values)

    @api.one
    def write(self, values):
        if self.is_operation and values.get('cost_center_account_code', False):
            # Overwrite existing name if cost_center is change
            values.update(name=values.get('cost_center_account_code'))

        return super(BudgetInheritOperation, self).write(values)

    # ACTION METHODS
    # ----------------------------------------------------------
    @api.multi
    def action_make_enhancement(self):
        action = super(BudgetInheritOperation, self).action_make_enhancement()
        context = action['context']
        context.update(default_is_operation_history=self.is_operation)
        action['context'] = context

        return action
