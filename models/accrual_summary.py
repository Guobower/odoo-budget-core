# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons.budget_core.models.utilities import choices_tuple

from odoo.exceptions import ValidationError, UserError


def create_accruals(env, date):
    contract_ids = env['budget.contractor.contract'].search([('is_opex', '=', True),
                                                             ('state','=', 'on going'),
                                                             ('commencement_date', '<=', date),
                                                             ('end_date', '>=', date)])

    data = []
    for contract_id in contract_ids:
        allocation_ids = contract_id.budget_contract_allocation_ids
        allocation_ids = allocation_ids.filtered(lambda r: r.budget_id.is_operation)
        if len(allocation_ids) == 0:
            continue

        elif len(allocation_ids) == 1:
            allocation_id = allocation_ids

        else:
            allocation_id = allocation_ids[0]

        values = {'contract_id': contract_id.id,
                  'budget_id': allocation_id.budget_id.id,
                  'date': date}
        data.append((0, 0, values))

    return False if not data else data


class AccrualSummary(models.Model):
    _name = 'budget.core.budget.accrual.summary'
    _rec_name = 'name'
    _description = 'Accrual Summary'
    _order = 'date'
    _inherit = ['record.lock.mixin']

    # CHOICES
    # ----------------------------------------------------------
    STATES = choices_tuple(['draft', 'approved'], is_sorted=False)

    # BASIC FIELDS
    # ----------------------------------------------------------
    state = fields.Selection(STATES, default='draft')

    date = fields.Date(string="Date", default=fields.Date.today())
    remarks = fields.Text(string="Remarks")
    active = fields.Boolean(default=True, help="Set active to false to hide the tax without removing it.")

    # RELATIONSHIPS
    # ----------------------------------------------------------
    company_currency_id = fields.Many2one('res.currency', readonly=True,
                                          default=lambda self: self.env.user.company_id.currency_id)

    # COMPUTE FIELDS
    # ----------------------------------------------------------
    accrual_ids = fields.One2many('budget.core.budget.accrual',
                                  'accrual_summary_id',
                                  string='Budget')

    name = fields.Char(string="Name",
                       compute="_compute_name",
                       store=True
                       )

    total_draft = fields.Integer(string='Total Draft Count',
                                 compute='_compute_total_draft',
                                 store=True)
    total_verified = fields.Integer(string='Total Verified Count',
                                    compute='_compute_total_verified',
                                    store=True)
    total_approved = fields.Integer(string='Total Approved Count',
                                    compute='_compute_total_approved',
                                    store=True)

    @api.one
    @api.depends('date')
    def _compute_name(self):
        if self.date:
            self.name = '{}'.format(fields.Datetime.from_string(self.date).strftime("%b-%Y"))

    @api.one
    @api.depends('accrual_ids', 'accrual_ids.state')
    def _compute_total_draft(self):
        self.total_draft = len(self.accrual_ids.filtered(lambda r: r.state == 'draft'))

    @api.one
    @api.depends('accrual_ids', 'accrual_ids.state')
    def _compute_total_verified(self):
        self.total_verified = len(self.accrual_ids.filtered(lambda r: r.state == 'verified'))

    @api.one
    @api.depends('accrual_ids', 'accrual_ids.state')
    def _compute_total_approved(self):
        self.total_approved = len(self.accrual_ids.filtered(lambda r: r.state == 'approved'))

    # RECORD LOCK CONDITION
    # ----------------------------------------------------------
    @api.one
    @api.depends('state')
    def _compute_is_record_lock(self):
        lock_states = ['approved']
        self.is_record_lock = True if self.state in lock_states else False

    # CONSTRAINS
    # ----------------------------------------------------------
    _sql_constraints = [
        ('name_uniq', 'UNIQUE (name)', 'Name Must be Uniq')
    ]

    # BUTTONS/TRANSITIONS
    # ----------------------------------------------------------
    @api.one
    def set2approved(self):
        accrual_ids = self.mapped('accrual_ids')

        accrual_states = self.mapped('accrual_ids.state')
        if 'draft' in accrual_states:
            raise ValidationError('There are still unverified Accruals')

        for accrual_id in accrual_ids:
            accrual_id.set2approved()

        self.state = 'approved'
        # OVERWRITE METHODS

    # ----------------------------------------------------------

    @api.model
    @api.returns('self', lambda value: value.id)
    def create(self, values):
        res = super(AccrualSummary, self).create(values)
        accrual_ids = create_accruals(self.env, res.date)
        res.update({'accrual_ids': accrual_ids})
        return res
