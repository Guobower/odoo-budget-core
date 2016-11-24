# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

from odoo.addons.my_utilities.models import choices_tuple


class BudgetHistoryInherit(models.Model):
    _inherit = 'budget.core.budget.history'
    _description = 'Budget History'

    # BASIC FIELDS
    # ----------------------------------------------------------
    is_project_history = fields.Boolean(string='Is Project History')
    commitment_amount = fields.Monetary(currency_field='company_currency_id',
                                         string='Commitment Amount')
