# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

from odoo.addons.budget_utilities.models.utilities import choices_tuple


class BudgetHistoryInheritProject(models.Model):
    _inherit = 'budget.core.budget.history'

    # BASIC FIELDS
    # ----------------------------------------------------------
    is_project_history = fields.Boolean(string='Is Project History')
    commitment_amount = fields.Monetary(currency_field='currency_id',
                                         string='Commitment Amount')


    # CONSTRAINS
    # ----------------------------------------------------------
    _sql_constraints = [
        ('commitment_must_not_be_negative', 'CHECK (commitment_amount >= 0)', 'Expenditure Amount Must Be Positive')
    ]


    @api.one
    @api.constrains('from_budget_id', 'commitment_amount')
    def _check_transfer_commitment(self):
        # action_taken and from_budget_id exist in budget.history
        # Checks of the sum of all commitment amount is 0 and raise an error
        if self.action_taken == 'transfer' and self.from_budget_id.commitment_amount < 0:
            raise ValidationError(_('Transfer of {:,.2f} from {} to {} is not possible,'
                                    ' total commitment amount will be {:,.2f}'. \
                                    format(self.commitment_amount, self.from_budget_id.name, self.to_budget_id.name,
                                           self.from_budget_id.commitment_amount)))
