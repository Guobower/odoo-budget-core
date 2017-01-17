# -*- coding: utf-8 -*-

from odoo import models, fields
from odoo.addons.budget_utilities.models.utilities import choices_tuple

class CostCenter(models.Model):
    _name = 'budget.core.account.code'
    _rec_name = 'account_code'

    # CHOICES
    # ----------------------------------------------------------
    STATES = choices_tuple(['draft', 'active', 'closed', 'cancelled'], is_sorted=False)

    # BASIC FIELDS
    # ----------------------------------------------------------
    state = fields.Selection(STATES, default='draft')
    account_code = fields.Char(string='Account Code')
    description = fields.Char(string='Description')

    # RELATIONSHIPS
    # ----------------------------------------------------------
    budget_ids = fields.One2many('budget.core.budget',
                                 'account_code_id',
                                 string="CC-AC")
