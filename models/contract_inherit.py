# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError

from odoo.tools import float_compare


class ContractInherit(models.Model):
    _inherit = 'budget.contractor.contract'

    # RELATIONSHIPS
    # ----------------------------------------------------------
    budget_contract_allocation_ids = fields.One2many('budget.core.contract.allocation',
                                                     'contract_id',
                                                     string="Budget Contract Allocation")

    accrual_ids = fields.One2many('budget.core.budget.accrual',
                                  'contract_id',
                                  string="Accrual")

    # ONCHANGE FIELDS
    # ----------------------------------------------------------
    @api.multi
    @api.onchange('budget_contract_allocation_ids', 'is_opex', 'is_capex')
    def onchange_budget_allocation_ids(self):
        self.section_ids |= self.mapped('budget_contract_allocation_ids.budget_id.section_id')
        self.sub_section_ids |= self.mapped('budget_contract_allocation_ids.budget_id.sub_section_id')

    @api.one
    def set2contract_signed(self):
        # state is already in contract
        # override this function in the main contract model
        # add a validation before changing state
        budget_ids = self.budget_contract_allocation_ids.mapped('budget_id')

        if self.is_opex and len(budget_ids.filtered(lambda r: r.is_operation)) == 0:
            raise ValidationError('Please fill up Opex Budget')

        if self.is_capex and len(budget_ids.filtered(lambda r: r.is_project)) == 0:
            raise ValidationError('Please fill up Capex Budget')

        super(ContractInherit, self).set2contract_signed()

        # CONSTRAINS
        # ----------------------------------------------------------
        # @api.one
        # @api.constrains('amount', 'budget_contract_allocation_ids')
        # def _check_required_amount(self):
        #     required_amount = sum(self.budget_contract_allocation_ids.mapped('required_amount'))
        #     if float_compare(self.amount, required_amount, precision_digits=2) != 0:
        #         msg = 'Contract Amount is {}, Total Required must be equal'.format(self.amount)
        #         raise ValidationError(msg)
