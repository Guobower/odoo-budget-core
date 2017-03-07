# -*- coding: utf-8 -*-

from odoo import models, fields
from odoo.addons.budget_utilities.models.utilities import choices_tuple


class AreaSpent(models.Model):
    _name = 'budget.core.account.code.area.spent'
    _rec_name = 'name'

    # CHOICES
    # ----------------------------------------------------------
    LEVELS = choices_tuple(['high', 'low'])

    # BASIC FIELDS
    # ----------------------------------------------------------
    level = fields.Selection(string='level', selection=LEVELS)
    name = fields.Char(string='Name')


