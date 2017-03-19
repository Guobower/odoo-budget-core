# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons.budget_core.models.utilities import choices_tuple

from odoo.exceptions import ValidationError, UserError

class AccrualSummaryInheritOperation(models.Model):
    _inherit = 'budget.core.budget.accrual.summary'

    # CHOICES
    # ----------------------------------------------------------

    # BASIC FIELDS
    # ----------------------------------------------------------
    is_operation_accrual_summary = fields.Boolean()

    # RELATIONSHIPS
    # ----------------------------------------------------------

    # COMPUTE FIELDS
    # ----------------------------------------------------------

    # CONSTRAINS
    # ----------------------------------------------------------

    # BUTTONS/TRANSITIONS
    # ----------------------------------------------------------

    # ----------------------------------------------------------
