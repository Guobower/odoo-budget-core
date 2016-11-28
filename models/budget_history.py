# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

from utilities import choices_tuple


class BudgetHistory(models.Model):
    _name = 'budget.core.budget.history'
    _rec_name = 'name'
    _description = 'Budget History'
    _order = 'change_date'

    # CHOICES
    # ----------------------------------------------------------
    OPTIONS = choices_tuple(['add', 'subtract', 'transfer'], is_sorted=False)

    # BASIC FIELDS
    # ----------------------------------------------------------
    name = fields.Char(string='Name')
    is_initial = fields.Boolean(string='Is Initial')

    action_taken = fields.Selection(string='Action Taken', selection=OPTIONS, default='add')
    expenditure_amount = fields.Monetary(currency_field='company_currency_id',
                                         string='Expenditure Amount')
    change_date = fields.Date(string="Change Date")
    remarks = fields.Text(string="Remarks")

    # RELATIONSHIPS
    # ----------------------------------------------------------
    company_currency_id = fields.Many2one('res.currency', readonly=True,
                                          default=lambda self: self.env.user.company_id.currency_id)

    budget_ids = fields.Many2many('budget.core.budget', 'budget_core_budget_history_rel', 'history_id', 'budget_id')
    from_budget_id = fields.Many2one('budget.core.budget',
                                     string="From Budget No")
    to_budget_id = fields.Many2one('budget.core.budget',
                                   string="To Budget No")

    # CONSTRAINS
    # ----------------------------------------------------------
    _sql_constraints = [
        ('expenditure_must_not_be_negative', 'CHECK (expenditure_amount >= 0)', 'Expenditure Amount Must Be Positive')
    ]

    @api.one
    @api.constrains('from_budget_id', 'expenditure_amount')
    def _check_transfer(self):
        # Checks of the sum of all expenditure amount is 0 and raise an error
        if self.action_taken == 'transfer' and self.from_budget_id.expenditure_amount < 0:
            raise ValidationError(_('Transfer of {:.2f} from {} to {} is not possible,'
                                    ' total expenditure will be amount is {:.2f}'.\
                                    format(self.expenditure_amount, self.from_budget_id.name, self.to_budget_id.name,
                                           self.from_budget_id.expenditure_amount)))

    # OVERRIDE METHODS
    # ----------------------------------------------------------
    @api.model
    @api.returns('self', lambda rec: rec.id)
    def create(self, values):

        to_budget_id = values.get('to_budget_id', False)
        from_budget_id = values.get('from_budget_id', False)
        if to_budget_id or from_budget_id:
            budget_ids = [x for x in [to_budget_id, from_budget_id] if x]
            values.update(budget_ids=[(6, 0, budget_ids)])
        return super(BudgetHistory, self).create(values)

    @api.one
    def write(self, values):
        to_budget_id = values.get('to_budget_id', self.to_budget_id.id)
        from_budget_id = values.get('from_budget_id', self.from_budget_id.id)
        budget_ids = [x for x in [to_budget_id, from_budget_id] if x]
        values.update(budget_ids=[(6, 0, budget_ids)])
        return super(BudgetHistory, self).write(values)

    @api.onchange('action_taken', 'to_budget_id', 'from_budget_id')
    def onchange_name(self):
        if self.action_taken in ['add', 'subtract']:
            self.name = '{}: {}'.format(self.action_taken.upper(), self.to_budget_id.name)

        elif self.action_taken == 'transfer':
            self.name = '{}: {} > {}'.format(self.action_taken.upper() or '',
                                             self.from_budget_id.name or '',
                                             self.to_budget_id.name or '')
