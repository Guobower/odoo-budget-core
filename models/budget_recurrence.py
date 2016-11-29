# -*- coding: utf-8 -*-

from odoo import models, fields, api


class BudgetRecurrence(models.Model):
    _name = 'budget.core.budget.recurrence'
    _rec_name = 'name'
    _description = 'Budget Recurrence'
    _order = 'recurrence_date'

    # CHOICES
    # ----------------------------------------------------------

    # BASIC FIELDS
    # ----------------------------------------------------------
    recurrence_amount = fields.Monetary(currency_field='company_currency_id',
                                        string='Recurrence Amount')
    recurrence_date = fields.Date(string="Recurrence Date")
    remarks = fields.Text(string="Remarks")


    # RELATIONSHIPS
    # ----------------------------------------------------------
    company_currency_id = fields.Many2one('res.currency', readonly=True,
                                          default=lambda self: self.env.user.company_id.currency_id)

    budget_id = fields.Many2one('budget.core.budget', string='Budget')

    # CONSTRAINS
    # ----------------------------------------------------------
    _sql_constraints = [
        ('recurrence_must_not_be_negative', 'CHECK (recurrence_amount >= 0)', 'Recurrence Amount Must Be Positive')
    ]

    # COMPUTE FIELDS
    # ----------------------------------------------------------
    name = fields.Char(compute="_compute_name",
                       string="Name")


    @api.one
    @api.depends('recurrence_date')
    def _compute_name(self):
        if self.recurrence_date:
            self.name = '{}'.format(fields.Datetime.from_string(self.recurrence_date).strftime("%b-%Y"))
