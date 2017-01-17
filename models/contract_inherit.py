# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.addons.budget_utilities.models.utilities import choices_tuple, int_to_roman


class ContractInherit(models.Model):
    _inherit = 'budget.contractor.contract'

    # RELATIONSHIPS
    # ----------------------------------------------------------
    budget_ids = fields.Many2many('budget.core.budget',
                                  'budget_contract_rel',
                                  'contract_id',
                                  'budget_id',
                                  string='Budgets')
