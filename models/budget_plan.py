# -*- coding: utf-8 -*-

from odoo import models, fields, api


class BudgetPlan(models.Model):
    _name = 'budget.core.budget.plan'
    _rec_name = 'name'
    _description = 'Budget Plan'
    _order = 'date'

    # CHOICES
    # ----------------------------------------------------------

    # BASIC FIELDS
    # ----------------------------------------------------------
    approved_amount = fields.Monetary(currency_field='company_currency_id',
                                        string='Approved Amount')
    deducted_amount = fields.Monetary(currency_field='company_currency_id',
                                        string='Deducted Amount')
    shared_amount = fields.Monetary(currency_field='company_currency_id',
                                        string='Shared Amount')
    date = fields.Date(string="Date")
    remarks = fields.Text(string="Remarks")

    # RELATIONSHIPS
    # ----------------------------------------------------------
    company_currency_id = fields.Many2one('res.currency', readonly=True,
                                          default=lambda self: self.env.user.company_id.currency_id)

    budget_id = fields.Many2one('budget.core.budget', string='Budget')

    # COMPUTE FIELDS
    # ----------------------------------------------------------
    name = fields.Char(compute="_compute_name",
                       string="Name",
                       store=True
                       )

    @api.one
    @api.depends('date')
    def _compute_name(self):
        if self.date:
            self.name = '{}'.format(fields.Datetime.from_string(self.date).strftime("%b-%Y"))

    # CONSTRAINS
    # ----------------------------------------------------------
    _sql_constraints = [
        ('approved_amount_must_not_be_negative', 'CHECK (approved_amount >= 0)', 'Approved Amount Must Be Positive'),
        ('deducted_amount_must_not_be_negative', 'CHECK (deducted_amount >= 0)', 'Deducted Amount Must Be Positive'),
        ('shared_amount_must_not_be_negative', 'CHECK (shared_amount >= 0)', 'Shared Amount Must Be Positive'),
        ('name_uniq', 'UNIQUE (name)', 'Name Must be Uniq')
    ]

