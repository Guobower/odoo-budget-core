# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons.my_utilities.models import choices_tuple

# TODO MAKE A FUNCTION OF EITHER ON CHANGE OR DEPENDS TO REFLECT PROJECT NO TO NAME
class BudgetInheritProject(models.Model):
    _inherit = 'budget.core.budget'

    # BASIC FIELDS
    # ----------------------------------------------------------
    is_project = fields.Boolean(string='Is Project')

    project_no = fields.Char(string="Project No")
    # expenditure_amount exist in budget.core.budget already
    commitment_amount = fields.Monetary(currency_field='company_currency_id',
                                        string='Commitment Amount')

    # RELATIONSHIPS
    # ----------------------------------------------------------
    # company_currency_id exist in budget.core.budget already

