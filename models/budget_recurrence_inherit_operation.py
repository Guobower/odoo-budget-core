# -*- coding: utf-8 -*-

from odoo import models, fields, api


class BudgetRecurrenceInheritOperation(models.Model):
    _inherit = 'budget.core.budget.recurrence'

    # CHOICES
    # ----------------------------------------------------------

    # BASIC FIELDS
    # ----------------------------------------------------------
    is_operation_recurrence = fields.Boolean(string='Is Recurrence Operation')

    # RELATIONSHIPS
    # ----------------------------------------------------------

    # COMPUTE FIELDS
    # ----------------------------------------------------------
