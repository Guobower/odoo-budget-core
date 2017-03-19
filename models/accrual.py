# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

from odoo.addons.budget_core.models.utilities import choices_tuple


class Accrual(models.Model):
    _name = 'budget.core.budget.accrual'
    _rec_name = 'name'
    _description = 'Budget Accrual'
    _order = 'date'

    # CHOICES
    # ----------------------------------------------------------
    STATES = choices_tuple(['draft', 'verified', 'approved'], is_sorted=False)

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

    budget_id = fields.Many2one('budget.core.budget',
                                string='Budget',
                                domain=[('is_operation', '=', True)])

    accrual_summary_id = fields.Many2one('budget.core.budget.accrual.summary',
                                         string='Accrual Summary',
                                         ondelete='cascade')

    # COMPUTE FIELDS
    # ----------------------------------------------------------
    is_readonly = fields.Boolean(compute="_compute_is_readonly",
                                 inverse="_set_is_readonly",
                                 string="Is Lock",
                                 help="readonly when a criteria is met",
                                 store=True
                                 )

    accrued_amount = fields.Monetary(string='Accrued Amount',
                                     currency_field='company_currency_id',
                                     compute="_compute_accrued_amount",
                                     inverse="_set_accrued_amount",
                                     store=True)

    name = fields.Char(compute="_compute_name",
                       string="Name",
                       store=True
                       )

    @api.one
    @api.depends('state')
    def _compute_is_readonly(self):
        if self.state == 'approved':
            self.is_readonly = True
        else:
            self.is_readonly = False

    @api.one
    @api.depends('date')
    def _compute_name(self):
        if self.date:
            self.name = '{}'.format(fields.Datetime.from_string(self.date).strftime("%b-%Y"))

    @api.one
    @api.depends('budget_id')
    def _compute_accrued_amount(self):
        if len(self.budget_id) != 0:
            budget_plan = self.env['budget.core.budget.plan'].search([('budget_id', '=', self.budget_id.id),
                                                                      ('name', '=', self.name)])

            amounts = [i for i in [budget_plan.shared_amount, budget_plan.deducted_amount, budget_plan.approved_amount]
                       if i != 0]

            amount = 0.0 if not amounts else amounts[0]

            self.accrued_amount = amount

        else:
            self.accrued_amount = 0.0

    @api.one
    def _set_accrued_amount(self):
        return

    @api.one
    def _set_is_readonly(self):
        return

    # CONSTRAINS
    # ----------------------------------------------------------
    _sql_constraints = [
        ('approved_amount_must_not_be_negative', 'CHECK (accrued_amount >= 0)', 'Approved Amount Must Be Positive'),
        ('name_budget_id_uniq', 'UNIQUE (name, budget_id)', 'Name Budget ID Must be Uniq')
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
    @api.one
    def write(self, values):
        # TODO STUDY THE POSSIBILITY OF USING ACCESS RULES FOR THIS, and also for delete to be use only if no approved
        if self.is_readonly and not values:
            raise ValidationError(_('Editing This Record is not Allowed'))

        return super(Accrual, self).write(values)
