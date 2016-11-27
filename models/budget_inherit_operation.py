# -*- coding: utf-8 -*-

from odoo import models, fields, api
from utilities import choices_tuple


class BudgetInheritOperation(models.Model):
    _inherit = 'budget.core.budget'

    # BASIC FIELDS
    # ----------------------------------------------------------
    is_operation = fields.Boolean(string='Is Operation')

    cost_center_account_code = fields.Char(string="CC-AC")
    # initial_expenditure_amount exist in budget.core.budget already

    # RELATIONSHIPS
    # ----------------------------------------------------------
    # company_currency_id exist in budget.core.budget already
    # history_ids exist in budget.core.budget already

    # COMPUTE FIELDS
    # ----------------------------------------------------------
    # expenditure_amount exist in budget.core.budget

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
                'is_operation': True
            }

            values.update(history_ids=[(0, 0, history)])

            # Equate Project No to Name
            cost_center_account_code = values.get('cost_center_account_code', '')
            values.update(name=cost_center_account_code)

        return super(BudgetInheritOperation, self).create(values)


    @api.one
    def write(self, values):
        if self.is_operation:
            # Equate Project No to Name
            cost_center_account_code = self.cost_center_account_code
            values.update(name=cost_center_account_code)

        return super(BudgetInheritOperation, self).write(values)
