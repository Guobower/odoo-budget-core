# -*- coding: utf-8 -*-

from odoo import models, fields, api
from utilities import choices_tuple


class BudgetContractAllocation(models.Model):
    _name = 'budget.core.contract.allocation'
    _rec_name = 'budget_id'
    _description = 'Budget Allocation for Contract'
    _inherit = ['mail.thread']

    # CHOICES
    # ----------------------------------------------------------

    # BASIC FIELDS
    # ----------------------------------------------------------
    required_amount = fields.Monetary(currency_field='company_currency_id',
                                      string='Required Amount',
                                      default=0.00)
    # TODO MAKE A COMPUTE FIELD AND TAKE BUDGET (COMMITMENT AND SHARED)
    total_budget_amount = fields.Monetary(currency_field='company_currency_id',
                                      string='Total Budget Amount',
                                      default=0.00)
    # TODO MAKE A COMPUTE FIELD
    total_accrual_amount = fields.Monetary(currency_field='company_currency_id',
                                      string='Total Accrued Amount',
                                      default=0.00)
    # RELATIONSHIPS
    # ----------------------------------------------------------
    company_currency_id = fields.Many2one('res.currency', readonly=True,
                                          default=lambda self: self.env.user.company_id.currency_id)
    budget_id = fields.Many2one('budget.core.budget', string='CWP/CC-AC', ondelete='cascade',
                                domain="[('state','=','active')]")
    contract_id = fields.Many2one('budget.contractor.contract', string='Contract', ondelete='cascade')

    # COMPUTE FIELDS
    # ----------------------------------------------------------
    # total_available_amount = fields.Monetary(string='Total Available Amount',
    #                                          compute='_compute_total_available_amount',
    #                                          currency_field='company_currency_id',
    #                                          default=0.00,
    #                                          store=True)

    # @api.one
    # @api.depends('budget_id.budget_amount')
    # def _compute_total_available_amount(self):
    #     self.total_available_amount = sum(self.budget_id.mapped('budget_amount'))
    # TRANSITIONS
    # ----------------------------------------------------------

    # OVERRIDE METHODS
    # ----------------------------------------------------------
