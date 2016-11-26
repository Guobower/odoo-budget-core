# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

from odoo.addons.my_utilities.models import choices_tuple


class BudgetHistoryInherit(models.Model):
    _inherit = 'budget.core.budget.history'

    # BASIC FIELDS
    # ----------------------------------------------------------
    is_operation_history = fields.Boolean(string='Is Operation History')

