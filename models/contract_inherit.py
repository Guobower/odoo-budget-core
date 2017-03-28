# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.addons.budget_utilities.models.utilities import choices_tuple, int_to_roman
from odoo.exceptions import ValidationError, UserError

from odoo.tools import float_compare

class ContractInherit(models.Model):
    _inherit = 'budget.contractor.contract'

    # RELATIONSHIPS
    # ----------------------------------------------------------
    budget_contract_allocation_ids = fields.One2many('budget.core.contract.allocation',
                                                     'contract_id',
                                                     string="Budget Contract Allocation",
                                                     store=True)

    # CONSTRAINS
    # ----------------------------------------------------------
    # @api.one
    # @api.constrains('amount', 'budget_contract_allocation_ids')
    # def _check_required_amount(self):
    #     required_amount = sum(self.budget_contract_allocation_ids.mapped('required_amount'))
    #     if float_compare(self.amount, required_amount, precision_digits=2) != 0:
    #         msg = 'Contract Amount is {}, Total Required must be equal'.format(self.amount)
    #         raise ValidationError(msg)
