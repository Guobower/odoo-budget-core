# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

from odoo.addons.my_utilities.models import choices_tuple


class BudgetHistory(models.Model):
    _name = 'budget.core.budget.history'
    _rec_name = 'name'
    _description = 'Budget History'

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
                                     string="From Project No")
    to_budget_id = fields.Many2one('budget.core.budget',
                                   string="To Project No")

    # OVERRIDE METHODS
    # ----------------------------------------------------------
    @api.model
    @api.returns('self', lambda rec: rec.id)
    def create(self, values):
        history = super(BudgetHistory, self).create(values)
        budget_ids = history.to_budget_id + history.from_budget_id
        history.budget_ids = budget_ids
        return history

    @api.onchange('action_taken', 'to_budget_id', 'from_budget_id')
    def onchange_name(self):
        if self.action_taken in ['add', 'subtract']:
            self.name = '{}: {}'.format(self.action_taken.upper(), self.to_budget_id.name)

        elif self.action_taken == 'transfer':
            self.name = '{}: {} > {}'.format(self.action_taken.upper() or '',
                                             self.from_budget_id.name or '',
                                             self.to_budget_id.name or '')

            # TODO OVERRIDE WRITE TO REFLECT CHANGES IN to_budget_id and from_budget_id to budget_ids