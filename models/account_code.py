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
        '1a - direct staff cost',
        '8 - outsourcing cost',
        '1b - indirect staff cost',
        '9 - other operating cost',
        '4 - repairs & maintenance',
        '5a - general expenses',
        '1c - cost transfers'
    ])
    CLASSIFICATION_HIGH_LEVELS = choices_tuple([
        'cost transfers',
        'fte',
        'general expenses',
        'maintenance',
        'other operating cost',
        'resources',
        'support',
        'utilities'
    ])
    CLASSIFICATION_LOW_LEVELS = choices_tuple([
        'direct staff cost',
        'pte',
        'team based hire',
        'overtime',
        'indirect staff cost',
        'tad',
        'other operating cost',
        'entertainment',
        'sundry exp',
        'buildings',
        'line plant',
        'tools & test equipment',
        'consultancy',
        'write offs',
        'cost transfers',
        'network support',
        'server support',
        'software support',
        'general expenses',
        'efm',
        'access network',
        'professional fees',
        'repair & return',
        'fuel',
        'rental genset',
        'tower',
        'e&m equipment',
        'incentive',
        'mobile cow',
        'telephone',
        'digital tv',
        'cse maintenance',
        'fdh uplifting',
        'office equipment',
        'vsat/earth station',
        'contract staff',
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
