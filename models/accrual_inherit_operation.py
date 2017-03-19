# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons.budget_core.models.utilities import choices_tuple

class AccrualInheritOperation(models.Model):
    _inherit = 'budget.core.budget.accrual'

    # CHOICES
    # ----------------------------------------------------------

    # BASIC FIELDS
    # ----------------------------------------------------------
    is_operation_accrual = fields.Boolean()

    # RELATIONSHIPS
    # ----------------------------------------------------------

    # COMPUTE FIELDS
    # ----------------------------------------------------------

    # CONSTRAINS
    # ----------------------------------------------------------

    # BUTTONS/TRANSITIONS
    # ----------------------------------------------------------
