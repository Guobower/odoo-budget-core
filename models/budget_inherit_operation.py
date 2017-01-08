# -*- coding: utf-8 -*-

from odoo import models, fields, api
from utilities import choices_tuple


class BudgetInheritOperation(models.Model):
    _inherit = 'budget.core.budget'

    # CHOICES
    # ----------------------------------------------------------
    SPENT_AREAS = choices_tuple(['low_level', 'high_level'])

    # BASIC FIELDS
    # ----------------------------------------------------------
    is_operation = fields.Boolean(string='Is Operation')

    cost_center = fields.Char(string="Cost Center")
    area_spent = fields.Selection(string='Area Spent', selection=SPENT_AREAS)

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

    # CONSTRAINS
    # ----------------------------------------------------------
    _sql_constraints = [
        ('uniq_cost_center', 'UNIQUE (cost_center)', 'Cost Center')
    ]

    # OVERRIDE METHODS
    # ----------------------------------------------------------
    @api.model
    @api.returns('self', lambda rec: rec.id)
    def create(self, values):
        if values.get('is_operation', False):
            initial_expenditure_amount = values.get('initial_expenditure_amount', 0.00)
            start_date = values.get('start_date', False)
            cost_center = values.get('cost_center', '')
            # create Initial history
            history = {
                # name exist in budget.core.budget
                'name': 'INITIAL: %s' % cost_center,
                'remarks': 'initial amount',
                'expenditure_amount': initial_expenditure_amount,
                'action_taken': 'add',
                'change_date': start_date,
                'is_initial': True,
                'is_operation_history': True
            }

            values.update(history_ids=[(0, 0, history)])

            # Equate Project No to Name
            cost_center = values.get('cost_center', '')
            values.update(name=cost_center)

        return super(BudgetInheritOperation, self).create(values)

    @api.one
    def write(self, values):
        if self.is_operation and values.get('cost_center', False):
            # Overwrite existing name if cost_center is change
            values.update(name=values.get('cost_center'))

        return super(BudgetInheritOperation, self).write(values)
