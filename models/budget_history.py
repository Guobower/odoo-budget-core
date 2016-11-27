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
                                     string="From Budget No")
    to_budget_id = fields.Many2one('budget.core.budget',
                                   string="To Budget No")

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
