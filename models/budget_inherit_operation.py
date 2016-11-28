# -*- coding: utf-8 -*-

from odoo import models, fields, api
from utilities import choices_tuple


class BudgetInheritOperation(models.Model):
    _inherit = 'budget.core.budget'

    # BASIC FIELDS
    # ----------------------------------------------------------
    is_operation = fields.Boolean(string='Is Operation')

    cost_center_account_code = fields.Char(string="CC-AC")
    cost_center = fields.Char(string="Cost Center")
    account_code = fields.Char(string="Account Code")

    # initial_expenditure_amount exist in budget.core.budget already

    # RELATIONSHIPS
    # ----------------------------------------------------------
    # company_currency_id exist in budget.core.budget already
    # history_ids exist in budget.core.budget already

    # COMPUTE FIELDS
    # ----------------------------------------------------------
    # expenditure_amount exist in budget.core.budget

    # ONCHANGES
    # ----------------------------------------------------------
    # region_id exist in budget.core.budget
    @api.onchange('cost_center_account_code', 'cost_center', 'account_code')
    def onchange_cost_center_account_code(self):
        if self.is_operation:
            cost_center = self.cost_center or ''
            account_code = self.account_code or ''
            self.cost_center_account_code = '{}-{}'.format(cost_center.upper(),
                                                           account_code.upper())

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
            # Overwrite existing name if cost_center_account_code is change
            values.update(name=values.get('cost_center_account_code'))

        return super(BudgetInheritOperation, self).write(values)
