# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons.budget_utilities.models.utilities import choices_tuple


class BudgetContractAllocation(models.Model):
    _name = 'budget.core.contract.allocation'
    _rec_name = 'budget_id'
    _description = 'Budget Allocation for Contract'
    _inherit = ['mail.thread']

    # CHOICES
    # ----------------------------------------------------------

    # BASIC FIELDS
    # ----------------------------------------------------------
    cost_per_month = fields.Monetary(string='Cost per Month', currency_field='company_currency_id')
    cost_per_year = fields.Monetary(string='Cost per Year', currency_field='company_currency_id')
    required_amount = fields.Monetary(currency_field='company_currency_id',
                                      string='Required Amount',
                                      default=0.00)
    expense_description = fields.Text(string='Expense Description')

    # RELATIONSHIPS
    # ----------------------------------------------------------
    company_currency_id = fields.Many2one('res.currency', readonly=True,
                                          default=lambda self: self.env.user.company_id.currency_id)
    budget_id = fields.Many2one('budget.core.budget', string='CWP/CC-AC', ondelete='cascade')
    contract_id = fields.Many2one('budget.contractor.contract', string='Contract', ondelete='cascade')

    # COMPUTE FIELDS
    # ----------------------------------------------------------
    total_budget_amount = fields.Monetary(currency_field='company_currency_id',
                                          string='Total Budget Amount',
                                          compute='_compute_total_budget_amount',
                                          store=True
                                          )

    total_accrual_amount = fields.Monetary(currency_field='company_currency_id',
                                           string='Total Accrued Amount',
                                           compute='_compute_total_accrual_amount',
                                           store=True
                                           )

    @api.one
    @api.depends()
    def _compute_total_budget_amount(self):
        pass

    @api.one
    @api.depends()
    def _compute_total_accrual_amount(self):
        pass

    # TRANSITIONS
    # ----------------------------------------------------------

    # OVERRIDE METHODS
    # ----------------------------------------------------------
