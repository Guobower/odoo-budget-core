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

    # option exist in budget.history
    @api.onchange('option', 'commitment_amount')
    def onchange_commitment_amount(self):
        if self.option == 'add':
            self.commitment_amount *= -1 if self.commitment_amount < 0 else 1

        elif self.option == 'subtract':
            self.commitment_amount *= -1 if self.commitment_amount > 0 else 1
