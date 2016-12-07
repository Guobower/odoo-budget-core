# -*- coding: utf-8 -*-

from odoo import models, fields, api
from utilities import choices_tuple


class BudgetInvestmentArea(models.Model):
    _name = 'budget.core.budget.investment.area'
    _rec_name = 'name'

    name = fields.Char(string="Name")

    # RELATIONSHIPS
    # ----------------------------------------------------------
    budget_ids = fields.One2many('budget.core.budget',
                                  'budget_investment_area_id',
                                  string="Budget Investment Area")
