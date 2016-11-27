# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons.my_utilities.models import choices_tuple

class Budget(models.Model):
    _name = 'budget.core.budget'
    _rec_name = 'name'
    _description = 'Budget'

    # CHOICES
    # ----------------------------------------------------------
    STATES = choices_tuple(['draft', 'active', 'closed', 'cancelled'], is_sorted=False)

    # BASIC FIELDS
    # ----------------------------------------------------------
    state = fields.Selection(STATES, default='draft')

    name = fields.Char(string="Name")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    description = fields.Text(string="Description")
    initial_expenditure_amount = fields.Monetary(currency_field='company_currency_id',
                                                 string='Initial Expenditure Amount',
                                                 default=0.00)
    # RELATIONSHIPS
    # ----------------------------------------------------------
    company_currency_id = fields.Many2one('res.currency', readonly=True,
                                          default=lambda self: self.env.user.company_id.currency_id)
    section_id = fields.Many2one('res.partner', string='Section',
                                 domain=[('is_budget_section', '=', True)])
    sub_section_id = fields.Many2one('res.partner', string='Sub Section',
                                     domain=[('is_budget_sub_section', '=', True)])
    history_ids = fields.Many2many('budget.core.budget.history', 'budget_core_budget_history_rel', 'budget_id', 'history_id')

    # COMPUTE FIELDS
    # ----------------------------------------------------------
    expenditure_amount = fields.Monetary(compute='_compute_expenditure_amount',
                                         currency_field='company_currency_id',
                                         string='Expenditure Amount',
                                         store=True)

    @api.one
    @api.depends('history_ids', 'history_ids.expenditure_amount')
    def _compute_expenditure_amount(self):
        for history in self.history_ids:
            if history.action_taken in ['add']:
                self.expenditure_amount += history.expenditure_amount
            elif history.action_taken in ['subtract']:
                self.expenditure_amount -= history.expenditure_amount
            elif history.action_taken in ['transfer'] and self.id == history.to_budget_id.id:
                self.expenditure_amount += history.expenditure_amount
            elif history.action_taken in ['transfer'] and self.id == history.from_budget_id.id:
                self.expenditure_amount -= history.expenditure_amount

    # TRANSITIONS
    # ----------------------------------------------------------
    def set2draft(self):
        self.state = 'draft'

    def set2active(self):
        self.state = 'active'

    def set2close(self):
        self.state = 'closed'

    # OVERRIDE METHODS
    # ----------------------------------------------------------
    @api.model
    @api.returns('self', lambda rec: rec.id)
    def create(self, values):
        if not values.get('history_ids', False):

            initial_expenditure_amount = values.get('initial_expenditure_amount', 0.00)
            name = values.get('name', '')
            start_date = values.get('start_date', False)
            # create Initial history
            history = {
                'name': 'INITIAL: %s' % name,
                'remarks': 'initial amount',
                'expenditure_amount': initial_expenditure_amount,
                'action_taken': 'add',
                'change_date': start_date,
                'is_initial': True
            }

            values.update(history_ids=[(0, 0, history)])

        return super(Budget, self).create(values)