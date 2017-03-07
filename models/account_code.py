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

    # BASIC FIELDS
    # ----------------------------------------------------------
    state = fields.Selection(STATES, default='draft')
    account_code = fields.Char(string='Account Code')
    description = fields.Text(string='Description')
    remark = fields.Text(string='Remark')
    grouping = fields.Selection(selection=GROUPINGS, string='Grouping')

    # RELATIONSHIPS
    # ----------------------------------------------------------
    area_of_spend_ll_id = fields.Many2one('budget.core.account.code.area.spent',
                                          domain=[('level','=','low')],
                                          string='Area of Spent (LOW LEVEL)')
    area_of_spend_hl_id = fields.Many2one('budget.core.account.code.area.spent',
                                           domain=[('level', '=', 'high')],
                                           string='Area of Spent (HIGH LEVEL)')

    budget_ids = fields.One2many('budget.core.budget',
                                 'account_code_id',
                                 string="CC-AC")
