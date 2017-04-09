# -*- coding: utf-8 -*-

from odoo import models, fields, api
from utilities import choices_tuple


class BudgetContractAllocation(models.Model):
    _name = 'budget.core.rfq.allocation'
    _rec_name = 'budget_id'
    _description = 'Budget Allocation for RFQ'

    # CHOICES
    # ----------------------------------------------------------

    # BASIC FIELDS
    # ----------------------------------------------------------
    # RELATIONSHIPS
    # ----------------------------------------------------------
    company_currency_id = fields.Many2one('res.currency', readonly=True,
                                          default=lambda self: self.env.user.company_id.currency_id)
    budget_id = fields.Many2one('budget.core.budget', string='CWP/CC-AC', ondelete='cascade')
    rfq_id = fields.Many2one('budget.contractor.rfq', string='RFQ')

    # COMPUTE FIELDS
    # ----------------------------------------------------------

    # TRANSITIONS
    # ----------------------------------------------------------

    # OVERRIDE METHODS
    # ----------------------------------------------------------
