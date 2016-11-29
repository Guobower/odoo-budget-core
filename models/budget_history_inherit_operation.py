# -*- coding: utf-8 -*-

from odoo import models, fields

class BudgetHistoryInheritOperation(models.Model):
    _inherit = 'budget.core.budget.history'


    # BASIC FIELDS
    # ----------------------------------------------------------
    is_operation_history = fields.Boolean(string='Is Operation History')

