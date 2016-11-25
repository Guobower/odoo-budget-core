# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons.my_utilities.models import choices_tuple


class BudgetInheritProject(models.Model):
    _inherit = 'budget.core.budget'

    # BASIC FIELDS
    # ----------------------------------------------------------
    is_project = fields.Boolean(string='Is Project')

    project_no = fields.Char(string="Project No")
    # initial_expenditure_amount exist in budget.core.budget already
    initial_commitment_amount = fields.Monetary(currency_field='company_currency_id',
                                                 string='Initial Commitment Amount',
                                                 default=0.00)

    # RELATIONSHIPS
    # ----------------------------------------------------------
    # company_currency_id exist in budget.core.budget already
    # history_ids exist in budget.core.budget already

    # COMPUTE FIELDS
    # ----------------------------------------------------------
    # expenditure_amount exist in budget.core.budget
    commitment_amount = fields.Monetary(compute='_compute_commitment_amount',
                                         currency_field='company_currency_id',
                                         string='Commitment Amount',
                                         store=True)

    @api.one
    @api.depends('history_ids', 'history_ids.commitment_amount')
    def _compute_commitment_amount(self):
        for history in self.history_ids:
            if history.action_taken in ['add']:
                self.commitment_amount += history.commitment_amount
            elif history.action_taken in ['subtract']:
                self.commitment_amount -= history.commitment_amount
            elif history.action_taken in ['transfer'] and self.id == history.to_budget_id.id:
                self.commitment_amount += history.commitment_amount
            elif history.action_taken in ['transfer'] and self.id == history.from_budget_id.id:
                self.commitment_amount -= history.commitment_amount

    # OVERRIDE METHODS
    # ----------------------------------------------------------
    @api.model
    @api.returns('self', lambda rec: rec.id)
    def create(self, values):
        if values.get('is_project', False):
            initial_expenditure_amount = values.get('initial_expenditure_amount', 0.00)
            initial_commitment_amount = values.get('initial_commitment_amount', 0.00)
            start_date = values.get('start_date', False)
            project_no = values.get('project_no', '')
            # create Initial history
            history = {
                # name exist in budget.core.budget
                'name': 'INITIAL: %s' % project_no,
                'remarks': 'initial amount',
                'expenditure_amount': initial_expenditure_amount,
                'commitment_amount': initial_commitment_amount,
                'action_taken': 'add',
                'change_date': start_date,
                'is_initial': True,
                'is_project_history': True
            }

            values.update(history_ids=[(0, 0, history)])

            # Equate Project No to Name
            project_no = values.get('project_no', '')
            values.update(name=project_no)

        return super(BudgetInheritProject, self).create(values)


    @api.one
    def write(self, values):
        if self.is_project:
            # Equate Project No to Name
            project_no = self.project_no
            values.update(name=project_no)

        return super(BudgetInheritProject, self).write(values)
