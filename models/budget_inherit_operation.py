# -*- coding: utf-8 -*-

from odoo import models, fields, api
from utilities import choices_tuple


class BudgetInheritOperation(models.Model):
    _inherit = 'budget.core.budget'

    # CHOICES
    # ----------------------------------------------------------
    SPENT_AREAS = choices_tuple(['low_level', 'high_level'])
    GROUPINGS = choices_tuple([
        '1a - Direct Staff Cost',
        '8 - Outsourcing Cost',
        '1b - Indirect Staff Cost',
        '9 - Other Operating Cost',
        '4 - Repairs & Maintenance',
        '5a - General Expenses',
        '1c - Cost Transfers'
    ])
    CLASSIFICATION_HIGH_LEVELS = choices_tuple([
        'FTE',
        'Resources',
        'Other Operating Cost',
        'Maintenance',
        'General Expenses',
        'Cost Transfers',
        'Support',
        'Utilities'
    ])
    CLASSIFICATION_LOW_LEVELS = choices_tuple([
        'Direct Staff Cost',
        'PTE',
        'Team based Hire',
        'Overtime',
        'Indirect Staff Cost',
        'TAD',
        'Other Operating Cost',
        'Entertainment',
        'Sundry Exp',
        'Buildings',
        'Line Plant',
        'Tools & Test Equipment',
        'Consultancy',
        'Write Offs',
        'Cost Transfers',
        'Network Support',
        'Server Support',
        'Software Support',
        'General Expenses',
        'eFM',
        'Access Network',
        'Professional Fees',
        'Repair & Return',
        'Fuel',
        'Rental Genset',
        'Tower',
        'E&M Equipment',
        'Incentive',
        'Mobile COW',
        'Telephone',
        'Digital TV',
        'CSE Maintenance',
        'FDH Uplifting',
        'Office Equipment',
        'VSAT/Earth Station',
        'Contract Staff',
    ])

    # BASIC FIELDS
    # ----------------------------------------------------------
    is_operation = fields.Boolean(string='Is Operation')

    cost_center_account_code = fields.Char(string="CC-AC")
    grouping = fields.Selection(string='Grouping', selection=GROUPINGS)
    classification_hl = fields.Selection(string='High Level', selection=CLASSIFICATION_HIGH_LEVELS)
    classification_ll = fields.Selection(string='Low Level', selection=CLASSIFICATION_LOW_LEVELS)
    area_spent = fields.Selection(string='Area Spent', selection=SPENT_AREAS)

    # initial_expenditure_amount exist in budget.core.budget already

    # RELATIONSHIPS
    # ----------------------------------------------------------
    # company_currency_id exist in budget.core.budget already
    # history_ids exist in budget.core.budget already
    cost_center_id = fields.Many2one('budget.core.cost.center', string='Cost Center')
    account_code_id = fields.Many2one('budget.core.account.code', string='Account Code')

    # RELATED FIELDS
    # ----------------------------------------------------------
    # company_currency_id exist in budget.core.budget already
    # history_ids exist in budget.core.budget already
    cost_center_description = fields.Char(related='cost_center_id.description',
                                          string='Cost Center Description',
                                          readonly=True)
    account_code_description = fields.Char(related='account_code_id.description',
                                           string='Account Code Description',
                                           readonly=True)

    # COMPUTE FIELDS
    # ----------------------------------------------------------
    # expenditure_amount exist in budget.core.budget

    # ONCHANGES
    # ----------------------------------------------------------
    # region_id exist in budget.core.budget
    @api.onchange('cost_center_account_code', 'cost_center_id', 'account_code_id')
    def onchange_cost_center_account_code(self):
        if self.is_operation:
            cost_center = self.cost_center_id.cost_center or ''
            account_code = self.account_code_id.account_code or ''
            self.cost_center_account_code = '{}-{}'.format(cost_center,
                                                           account_code)

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
