# -*- coding: utf-8 -*-

from odoo import models, fields, api


class BudgetPlanInheritOperation(models.Model):
    _inherit = 'budget.core.budget.plan'

    # CHOICES
    # ----------------------------------------------------------

    # BASIC FIELDS
    # ----------------------------------------------------------
    is_operation_plan = fields.Boolean(string='Is Plan Operation')

    # RELATIONSHIPS
    # ----------------------------------------------------------

    # COMPUTE FIELDS
    # ----------------------------------------------------------
