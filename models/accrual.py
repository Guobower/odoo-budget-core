# -*- coding: utf-8 -*-
import datetime
import dateutil.relativedelta

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

from odoo.addons.budget_core.models.utilities import choices_tuple


class Accrual(models.Model):
    _name = 'budget.core.budget.accrual'
    _rec_name = 'name'
    _description = 'Budget Accrual'
    _order = 'date'
    _inherit = ['record.lock.mixin']

    # CHOICES
    # ----------------------------------------------------------
    STATES = choices_tuple(['draft', 'verified', 'approved'], is_sorted=False)

    # BASIC FIELDS
    # ----------------------------------------------------------
    state = fields.Selection(STATES, default='draft')

    date = fields.Date(string="Date")
    remarks = fields.Text(string="Remarks")
    active = fields.Boolean(default=True, help="Set active to false to hide the tax without removing it.")

    # RELATED FIELDS
    # ----------------------------------------------------------
    contract_description = fields.Text(related='contract_id.description')

    previous_accrued_amount = fields.Monetary(string='Previous Accrued Amount',
                                              currency_field='company_currency_id',
                                              related='previous_accrual_id.accrued_amount',
                                              store=True)

    # RELATIONSHIPS
    # ----------------------------------------------------------
    company_currency_id = fields.Many2one('res.currency', readonly=True,
                                          default=lambda self: self.env.user.company_id.currency_id)

    budget_id = fields.Many2one('budget.core.budget',
                                string='Budget'
                                )

    contract_id = fields.Many2one('budget.contractor.contract',
                                  string='Contract')

    accrual_summary_id = fields.Many2one('budget.core.budget.accrual.summary',
                                         string='Accrual Summary',
                                         ondelete='cascade')

    # COMPUTE FIELDS
    # ----------------------------------------------------------
    name = fields.Char(compute="_compute_name",
                       string="Name",
                       store=True
                       )

    previous_accrual_id = fields.Many2one('budget.core.budget.accrual',
                                          string='Previous_accrual',
                                          compute='_compute_previous_accrual_id',
                                          store=True)

    accrued_amount = fields.Monetary(string='Accrued Amount',
                                     currency_field='company_currency_id',
                                     compute='_compute_accrued_amount',
                                     inverse='_set_accrued_amount',
                                     store=True
                                     )

    @api.one
    @api.depends('date')
    def _compute_name(self):
        if self.date:
            self.name = '{}'.format(fields.Datetime.from_string(self.date).strftime("%b-%Y"))

    @api.one
    @api.depends('name', 'budget_id', 'contract_id')
    def _compute_previous_accrual_id(self):
        if not self.name:
            return
        date = datetime.datetime.strptime(self.date, "%Y-%m-%d")
        date -= dateutil.relativedelta.relativedelta(months=1)

        name = date.strftime("%b-%Y")
        previous_accrual_id = self.search([('name', '=', name),
                                           ('contract_id', '=', self.contract_id.id),
                                           ('budget_id', '=', self.budget_id.id)])
        self.previous_accrual_id = previous_accrual_id

    @api.one
    @api.depends('contract_id', 'budget_id')
    def _compute_accrued_amount(self):
        if not self.contract_id and not self.budget_id:
            return
        cost_per_month = self.env['budget.core.contract.allocation']. \
            search([('contract_id', '=', self.contract_id.id),
                    ('budget_id', '=', self.budget_id.id)]).cost_per_month
        self.accrued_amount = cost_per_month

    # RECORD LOCK CONDITION
    # ----------------------------------------------------------
    @api.one
    @api.depends('state')
    def _compute_is_record_lock(self):
        lock_states = ['approved']
        self.is_record_lock = True if self.state in lock_states else False

    @api.one
    def _set_accrued_amount(self):
        return

    # CONSTRAINS
    # ----------------------------------------------------------
    # TODO REMOVE name_budget_id_uniq after updating production
    _sql_constraints = [
        ('approved_amount_must_not_be_negative', 'CHECK (accrued_amount >= 0)', 'Approved Amount Must Be Positive'),
        ('name_budget_id_uniq', 'CHECK(1=1)', 'Name Budget ID Must be Uniq'),
        ('identifier_uniq', 'UNIQUE (name, budget_id, contract_id)', 'Name Budget ID Contract Must be Uniq')
    ]

    # BUTTONS/TRANSITIONS
    # ----------------------------------------------------------
    @api.multi
    def set2verified(self):
        for record in self:
            record.state = 'verified'

    @api.multi
    def set2approved(self):
        for record in self:
            record.state = 'approved'

    # OVERRIDE METHODS
    # ----------------------------------------------------------
