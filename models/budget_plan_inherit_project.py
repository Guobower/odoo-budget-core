# -*- coding: utf-8 -*-

from odoo import models, fields, api


class BudgetPlanInheritProject(models.Model):
    _inherit = 'budget.core.budget.plan'

    # CHOICES
    # ----------------------------------------------------------

    # BASIC FIELDS
    # ----------------------------------------------------------
    is_project_plan = fields.Boolean(string='Is Plan Project')
    commitment_amount = fields.Monetary(currency_field='company_currency_id',
                                        string='Commitment Amount')
    # RELATIONSHIPS
    # ----------------------------------------------------------

    # CONSTRAINS
    # ----------------------------------------------------------
    _sql_constraints = [
        ('commitment_must_not_be_negative', 'CHECK (commitment_amount >= 0)', 'Commitment Amount Must Be Positive')
    ]

    # COMPUTE FIELDS
    # ----------------------------------------------------------
