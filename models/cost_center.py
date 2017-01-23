# -*- coding: utf-8 -*-

from odoo import models, fields
from odoo.addons.budget_utilities.models.utilities import choices_tuple

class CostCenter(models.Model):
    _name = 'budget.core.cost.center'
    _rec_name = 'cost_center'

    # CHOICES
    # ----------------------------------------------------------
    STATES = choices_tuple(['draft', 'active', 'closed', 'cancelled'], is_sorted=False)

    # BASIC FIELDS
    # ----------------------------------------------------------
    state = fields.Selection(STATES, default='draft')
    cost_center = fields.Char(string='Cost Center')
    description = fields.Text(string='Description')
    remark = fields.Text(string='Remark')

    # RELATIONSHIPS
    # ----------------------------------------------------------
    section_id = fields.Many2one('res.partner',
                                 domain=[('is_budget_section','=',True)],
                                 string="Section")
    sub_section_id = fields.Many2one('res.partner',
                                 domain=[('is_budget_sub_section','=',True)],
                                 string="Sub Section")
    budget_ids = fields.One2many('budget.core.budget',
                                 'cost_center_id',
                                 string="CC-AC")
