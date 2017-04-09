# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.addons.budget_utilities.models.utilities import choices_tuple, int_to_roman


class RfqInherit(models.Model):
    _inherit = 'budget.contractor.rfq'

    # CHOICES
    # ----------------------------------------------------------

    # BASIC FIELDS
    # ----------------------------------------------------------
    is_capex = fields.Boolean(string='Has Capex')
    is_opex = fields.Boolean(string='Has Opex')

    # RELATIONSHIPS
    # ----------------------------------------------------------
    budget_rfq_allocation_ids = fields.One2many('budget.core.rfq.allocation',
                                                'rfq_id',
                                                string="Budget RFQ Allocation")
    # ONCHANGE FIELDS
    # ----------------------------------------------------------

    # CONSTRAINS
    # ----------------------------------------------------------
