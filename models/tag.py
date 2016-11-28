# -*- coding: utf-8 -*-

from odoo import models, fields


class BudgetTags(models.Model):
    _name = 'budget.core.tag'
    _rec_name = 'name'

    # BASIC FIELDS
    # ----------------------------------------------------------
    is_budget_core_budget = fields.Boolean(string='Is Budget Core Budget')

    name = fields.Char(string='Tag Name')

    # RELATIONSHIPS
    # ----------------------------------------------------------
    budget_ids = fields.Many2many('budget.core.tag',
                                'budget_core_tags_rel',
                                'tag_id', 'budget_id')
