# -*- coding: utf-8 -*-

from odoo import models, fields
from odoo.addons.budget_utilities.models.utilities import choices_tuple


class AccountCode(models.Model):
    _name = 'budget.core.account.code'
    _rec_name = 'account_code'

    # CHOICES
    # ----------------------------------------------------------
    STATES = choices_tuple(['draft', 'active', 'closed', 'cancelled'], is_sorted=False)
    GROUPINGS = choices_tuple([
        '1a - Direct Staff Cost',
        '8 - Outsourcing Cost',
        '1b - Indirect Staff Cost',
        '9 - Other Operating Cost',
        '4 - Repairs & Maintenance',
        '5a - General Expenses',
        '1c - Cost Transfers'
    ])
    CLASSIFICATION_HIGH_LEVELS = choices_tuple([
        'FTE',
        'Resources',
        'Other Operating Cost',
        'Maintenance',
        'General Expenses',
        'Cost Transfers',
        'Support',
        'Utilities'
    ])
    CLASSIFICATION_LOW_LEVELS = choices_tuple([
        'Direct Staff Cost',
        'PTE',
        'Team based Hire',
        'Overtime',
        'Indirect Staff Cost',
        'TAD',
        'Other Operating Cost',
        'Entertainment',
        'Sundry Exp',
        'Buildings',
        'Line Plant',
        'Tools & Test Equipment',
        'Consultancy',
        'Write Offs',
        'Cost Transfers',
        'Network Support',
        'Server Support',
        'Software Support',
        'General Expenses',
        'eFM',
        'Access Network',
        'Professional Fees',
        'Repair & Return',
        'Fuel',
        'Rental Genset',
        'Tower',
        'E&M Equipment',
        'Incentive',
        'Mobile COW',
        'Telephone',
        'Digital TV',
        'CSE Maintenance',
        'FDH Uplifting',
        'Office Equipment',
        'VSAT/Earth Station',
        'Contract Staff',
    ])

    # BASIC FIELDS
    # ----------------------------------------------------------
    state = fields.Selection(STATES, default='draft')
    account_code = fields.Char(string='Account Code')
    description = fields.Text(string='Description')
    remark = fields.Text(string='Remark')
    grouping = fields.Selection(selection=GROUPINGS, string='Grouping')
    area_of_spend_ll = fields.Selection(selection=CLASSIFICATION_LOW_LEVELS,
                                        string='Area of Spent (LOW LEVEL)')
    area_of_spend_hl = fields.Selection(selection=CLASSIFICATION_HIGH_LEVELS,
                                        string='Area of Spent (HIGH LEVEL)')

    # RELATIONSHIPS
    # ----------------------------------------------------------
    budget_ids = fields.One2many('budget.core.budget',
                                 'account_code_id',
                                 string="CC-AC")
