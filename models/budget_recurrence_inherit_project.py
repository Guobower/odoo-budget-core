# -*- coding: utf-8 -*-

from odoo import models, fields, api


class BudgetRecurrenceInheritProject(models.Model):
    _inherit = 'budget.core.budget.recurrence'

    # CHOICES
    # ----------------------------------------------------------

    # BASIC FIELDS
    # ----------------------------------------------------------
    is_project_recurrence = fields.Boolean(string='Is Recurrence Project')

    # RELATIONSHIPS
    # ----------------------------------------------------------

    # COMPUTE FIELDS
    # ----------------------------------------------------------
