# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.addons.budget_utilities.models.utilities import choices_tuple


class BudgetInheritProject(models.Model):
    _inherit = 'budget.core.budget'

    # BASIC FIELDS
    # ----------------------------------------------------------
    is_project = fields.Boolean(string='Is Project')

    project_no = fields.Char(string="Project No")
    cwp = fields.Char(string="CWP")
    category = fields.Char(string="Category")
    remarks = fields.Text(string="Remarks")
    rfs_date = fields.Date(string="Ready for Service Date")
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

    # ONCHANGES
    # ----------------------------------------------------------
    # region_id exist in budget.core.budget
    @api.onchange('project_no', 'region_id', 'cwp', 'category', 'is_project')
    def onchange_project_no(self):
        if self.is_project:
            region = self.region_id.alias or ''
            cwp = self.cwp or ''
            category = self.category or ''
            string_list = [i for i in [region.upper(), cwp.upper(), category.upper()] if i is not '']
            self.project_no = '-'.join(string_list)

    # CONSTRAINS
    # TODO MUST BE REVIEWED AS MAJORITY OF CWP IS HAVE EXPENDITURE MORE THAN COMMITMENT
    # ----------------------------------------------------------
    # @api.one
    # @api.constrains('expenditure_amount', 'commitment_amount', 'is_project')
    # def _check_expenditure_commitment(self):
    #     """
    #     The Total Expenditure must not be greater than Total Commitment
    #     If it is a project
    #     """
    #     if self.is_project and self.expenditure_amount > self.commitment_amount:
    #         raise ValidationError("Expenditure Can't exceed Total Commitment")

    _sql_constraints = [
        ('uniq_project_no', 'UNIQUE (project_no)', 'Project No Must Be unique')
    ]


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
        if self.is_project and values.get('project_no', False):
            # Overwrite existing name if project_no is change
            values.update(name=values.get('project_no'))

        return super(BudgetInheritProject, self).write(values)

    # ACTION METHODS
    # ----------------------------------------------------------
    @api.multi
    def action_make_enhancement(self):
        action = super(BudgetInheritProject, self).action_make_enhancement()
        context = action['context']
        context.update(default_is_project_history=self.is_project)
        action['context'] = context

        return action
