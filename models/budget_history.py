# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

from odoo.addons.my_utilities.models import choices_tuple

# TODO REMOVE COMMITMENT IN THIS MODEL AND PLACE IT TO INHERITED HISTORY
# ALSO CHECK THE LOGIC FOR TRANSFER
class BudgetHistory(models.Model):
    _name = 'budget.core.budget.history'
    _description = 'Budget History'

    # CHOICES
    # ----------------------------------------------------------
    OPTIONS = choices_tuple(['add', 'subtract', 'transfer'], is_sorted=False)


    # BASIC FIELDS
    # ----------------------------------------------------------
    option = fields.Selection(string='Option', selection=OPTIONS)
    commitment_amount = fields.Monetary(currency_field='company_currency_id',
                                        string='Commitment Amount')
    expenditure_amount = fields.Monetary(currency_field='company_currency_id',
                                        string='Expenditure Amount')
    change_date = fields.Date(string="Change Date")
    remarks = fields.Text(string="Remarks")

    # RELATIONSHIPS
    # ----------------------------------------------------------
    company_currency_id = fields.Many2one('res.currency', readonly=True,
                                          default=lambda self: self.env.user.company_id.currency_id)

    budget_id = fields.Many2one('budget.core.budget')
    from_budget_id = fields.Many2one('budget.core.budget',
                                      string="From Project No")
    to_budget_id = fields.Many2one('budget.core.budget',
                                    string="To Project No")
    # # CONSTRAINS
    # # ----------------------------------------------------------
    # @api.one
    # @api.constrains('option', 'budget_id', 'from_budget_id', 'to_budget_id')
    # def _check_option(self):
    #     if self.option == 'transfer' and self.from_budget_id == self.to_budget_id:
    #         raise ValidationError(_("Transfer Option: From and To Project should not be equal"))
    #
    #     elif self.option == 'transfer' and self.budget_id.budget_no not in [self.to_budget_id.budget_no,
    #                                                                           self.to_budget_id.budget_no]:
    #         raise ValidationError(_("Transfer Option: Transfer is invalid %s must be in from or to" % self.budget_id.budget_no))

    @api.onchange('option', 'budget_id', 'from_budget_id', 'to_budget_id', 'commitment_amount', 'expenditure_amount')
    def onchange_option(self):
        if self.option == 'add':
            self.commitment_amount *= -1 if self.commitment_amount < 0 else 1
            self.expenditure_amount *= -1 if self.expenditure_amount < 0 else 1

        elif self.option == 'subtract':
            self.commitment_amount *= -1 if self.commitment_amount > 0 else 1
            self.expenditure_amount *= -1 if self.expenditure_amount > 0 else 1

        elif self.option == 'transfer':
            self.commitment_amount = abs(self.commitment_amount)
            self.expenditure_amount = abs(self.expenditure_amount)

            self.commitment_amount *= -1 if self.budget_id.budget_no == self.from_budget_id.budget_no else 1
            self.expenditure_amount *= -1 if self.budget_id.budget_no == self.from_budget_id.budget_no else 1
