# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

from odoo.addons.my_utilities.models import choices_tuple


class BudgetHistoryInherit(models.Model):
    _inherit = 'budget.core.budget.history'
    _description = 'Budget History'

    # BASIC FIELDS
    # ----------------------------------------------------------
    commitment_amount = fields.Monetary(currency_field='company_currency_id',
                                        string='Commitment Amount')

    # action_taken exist in budget.history
    @api.onchange('action_taken', 'commitment_amount')
    def onchange_commitment_amount(self):
        if self.action_taken == 'add':
            self.commitment_amount *= -1 if self.commitment_amount < 0 else 1

        elif self.action_taken == 'subtract':
            self.commitment_amount *= -1 if self.commitment_amount > 0 else 1
