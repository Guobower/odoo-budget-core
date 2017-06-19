# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons.budget_utilities.models.utilities import choices_tuple


class BudgetInvestmentArea(models.Model):
    _name = 'budget.core.budget.investment.area'
    _rec_name = 'name'

    name = fields.Char(string="Name")

    # RELATIONSHIPS
    # ----------------------------------------------------------
    budget_ids = fields.One2many('budget.core.budget',
                                  'investment_area_id',
                                  string="Budget Investment Area")
