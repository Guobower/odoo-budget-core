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
    expenditure_amount = fields.Monetary(currency_field='company_currency_id',
                                        string='Expenditure Amount')
    date = fields.Date(string="Date")
    remarks = fields.Text(string="Remarks")

    # RELATIONSHIPS
    # ----------------------------------------------------------
    company_currency_id = fields.Many2one('res.currency', readonly=True,
                                          default=lambda self: self.env.user.company_id.currency_id)

    budget_id = fields.Many2one('budget.core.budget', string='Budget')

    # CONSTRAINS
    # ----------------------------------------------------------
    _sql_constraints = [
        ('expenditure_must_not_be_negative', 'CHECK (expenditure_amount >= 0)', 'Expenditure Amount Must Be Positive')
    ]

    # COMPUTE FIELDS
    # ----------------------------------------------------------
    name = fields.Char(compute="_compute_name",
                       string="Name")

    @api.one
    @api.depends('date')
    def _compute_name(self):
        if self.date:
            self.name = '{}'.format(fields.Datetime.from_string(self.date).strftime("%b-%Y"))
