# -*- coding: utf-8 -*-
import datetime as dt
import pandas as pd
from odoo import models, fields, api
from odoo.addons.budget_utilities.models.utilities import choices_tuple, odoo_to_pandas_list
from odoo.addons.budget_utilities.xlsx_creator.creator import Creator

from odoo.exceptions import ValidationError, UserError


def get_accrual_amount(data=None, mn='', year=''):
    """
    res is accrual_ids
    mn is in %b format eg. Jan
    yr is year in string
    :return: value or 0.0 
    """
    if data is None:
        data = {}
    target_date = '{}-{}'.format(mn.capitalize(), year)

    if target_date is not None and target_date in data.keys():
        return data[target_date]
    else:
        return 0.0


def create_accruals(env, date):
    contract_ids = env['budget.contractor.contract'].search([('is_opex', '=', True),
                                                             ('state', '=', 'on going'),
                                                             ('commencement_date', '<=', date),
                                                             ('end_date', '>=', date)])

    data = []
    opex_allocation_ids = contract_ids.mapped('budget_contract_allocation_ids').filtered(
        lambda r: r.budget_id.is_operation)
    for opex_allocation_id in opex_allocation_ids:
        values = {'contract_id': opex_allocation_id.contract_id.id,
                  'budget_id': opex_allocation_id.budget_id.id,
                  'date': date}
        data.append((0, 0, values))

    return False if not data else data


class AccrualSummary(models.Model):
    _name = 'budget.core.budget.accrual.summary'
    _rec_name = 'name'
    _description = 'Accrual Summary'
    _order = 'date'
    _inherit = ['record.lock.mixin']

    # CHOICES
    # ----------------------------------------------------------
    STATES = choices_tuple(['draft', 'approved'], is_sorted=False)

    # BASIC FIELDS
    # ----------------------------------------------------------
    state = fields.Selection(STATES, default='draft')

    date = fields.Date(string="Date", default=fields.Date.today())
    remarks = fields.Text(string="Remarks")
    active = fields.Boolean(default=True, help="Set active to false to hide the tax without removing it.")

    # RELATIONSHIPS
    # ----------------------------------------------------------
    company_currency_id = fields.Many2one('res.currency', readonly=True,
                                          default=lambda self: self.env.user.company_id.currency_id)

    # COMPUTE FIELDS
    # ----------------------------------------------------------
    accrual_ids = fields.One2many('budget.core.budget.accrual',
                                  'accrual_summary_id',
                                  string='Budget')

    name = fields.Char(string="Name",
                       compute="_compute_name",
                       store=True
                       )

    total_draft = fields.Integer(string='Total Draft Count',
                                 compute='_compute_total_draft',
                                 store=True)
    total_verified = fields.Integer(string='Total Verified Count',
                                    compute='_compute_total_verified',
                                    store=True)
    total_approved = fields.Integer(string='Total Approved Count',
                                    compute='_compute_total_approved',
                                    store=True)

    @api.one
    @api.depends('date')
    def _compute_name(self):
        if self.date:
            self.name = '{}'.format(fields.Datetime.from_string(self.date).strftime("%b-%Y"))

    @api.one
    @api.depends('accrual_ids', 'accrual_ids.state')
    def _compute_total_draft(self):
        self.total_draft = len(self.accrual_ids.filtered(lambda r: r.state == 'draft'))

    @api.one
    @api.depends('accrual_ids', 'accrual_ids.state')
    def _compute_total_verified(self):
        self.total_verified = len(self.accrual_ids.filtered(lambda r: r.state == 'verified'))

    @api.one
    @api.depends('accrual_ids', 'accrual_ids.state')
    def _compute_total_approved(self):
        self.total_approved = len(self.accrual_ids.filtered(lambda r: r.state == 'approved'))

    # RECORD LOCK CONDITION
    # ----------------------------------------------------------
    @api.one
    @api.depends('state')
    def _compute_is_record_lock(self):
        lock_states = ['approved']
        self.is_record_lock = True if self.state in lock_states else False

    # CONSTRAINS
    # ----------------------------------------------------------
    _sql_constraints = [
        ('name_uniq', 'UNIQUE (name)', 'Name Must be Uniq')
    ]

    # BUTTONS/TRANSITIONS
    # ----------------------------------------------------------
    @api.one
    def set2approved(self):
        accrual_ids = self.mapped('accrual_ids')

        accrual_states = self.mapped('accrual_ids.state')
        if 'draft' in accrual_states:
            raise ValidationError('There are still unverified Accruals')

        for accrual_id in accrual_ids:
            accrual_id.set2approved()

        self.state = 'approved'

    @api.one
    def create_accrual_file(self):
        creator = Creator(filename=self.name,
                          form_filename='opex_accrual.xlsx',
                          module_name='budget_core',
                          res_id=self.id,
                          res_model=self._name)

        # WORK SHEET MAIN
        # ----------------------------------------------------------
        wb = creator.get_wb()
        ws = wb.get_sheet_by_name('main')
        row = 4
        column = 1
        sr = 1
        ws.cell('A1').value = ws.cell('A1').value + ' %s' % self.name

        # all Accruals
        accrual_ids = self.env['budget.core.budget.accrual'].search(
            [('date', '>=', dt.date(int(self.name[-4:]), 1, 1)),
             ('date', '<', dt.date(int(self.name[-4:]) + 1, 1, 1))])

        df_accrual = pd.DataFrame(odoo_to_pandas_list(accrual_ids, ['id', 'name', 'date', 'previous_accrued_amount',
                                                                    'accrued_amount', 'budget_id.id',
                                                                    'contract_id.id']))
        pivot_accrual = pd.pivot_table(df_accrual, values='accrued_amount', index=['budget_id.id', 'contract_id.id'],
                                       columns=['name'])
        pivot_accrual.fillna(0, inplace=True)
        rs_accrual = pivot_accrual.reset_index(level=['budget_id.id', 'contract_id.id']).to_dict('records')

        year = fields.Date.from_string(self.date).strftime('%Y')

        ws.insert_rows(row, len(rs_accrual) - 1)

        for r in rs_accrual:
            contract_id = self.env['budget.contractor.contract'].search([('id', '=', int(r['contract_id.id']))])
            budget_id = self.env['budget.core.budget'].search([('id', '=', int(r['budget_id.id']))])
            budget_contract_allocation_id = self.env['budget.core.contract.allocation'].search([
                ('contract_id', '=', int(r['contract_id.id'])),
                ('budget_id', '=', int(r['budget_id.id']))
            ])

            ws.cell(row=row, column=column).value = sr
            ws.cell(row=row, column=column + 1).value = budget_contract_allocation_id.expense_description
            ws.cell(row=row, column=column + 2).value = contract_id.contract_ref
            ws.cell(row=row, column=column + 3).value = contract_id.contractor_id.name
            ws.cell(row=row, column=column + 4).value = contract_id.amount
            ws.cell(row=row, column=column + 5).value = contract_id.year_count
            ws.cell(row=row, column=column + 6).value = get_accrual_amount(r, 'Jan', year)
            ws.cell(row=row, column=column + 7).value = get_accrual_amount(r, 'Feb', year)
            ws.cell(row=row, column=column + 8).value = get_accrual_amount(r, 'Mar', year)
            ws.cell(row=row, column=column + 9).value = get_accrual_amount(r, 'Apr', year)
            ws.cell(row=row, column=column + 10).value = get_accrual_amount(r, 'May', year)
            ws.cell(row=row, column=column + 11).value = get_accrual_amount(r, 'Jun', year)
            ws.cell(row=row, column=column + 12).value = get_accrual_amount(r, 'Jul', year)
            ws.cell(row=row, column=column + 13).value = get_accrual_amount(r, 'Aug', year)
            ws.cell(row=row, column=column + 14).value = get_accrual_amount(r, 'Sep', year)
            ws.cell(row=row, column=column + 15).value = get_accrual_amount(r, 'Oct', year)
            ws.cell(row=row, column=column + 16).value = get_accrual_amount(r, 'Nov', year)
            ws.cell(row=row, column=column + 17).value = get_accrual_amount(r, 'Dec', year)
            ws.cell(row=row, column=column + 19).value = int(budget_id.cost_center_id.cost_center)
            ws.cell(row=row, column=column + 20).value = int(budget_id.account_code_id.account_code)
            # TODO CHANGE SECTION ID TO DIVISION ID
            ws.cell(row=row, column=column + 22).value = budget_id.section_id.alias
            ws.cell(row=row, column=column + 23).value = budget_id.sub_section_id.name
            row += 1
            sr += 1

        creator.attach(self.env)

    # OVERWRITE METHODS
    # ----------------------------------------------------------
    @api.model
    @api.returns('self', lambda value: value.id)
    def create(self, values):
        res = super(AccrualSummary, self).create(values)
        accrual_ids = create_accruals(self.env, res.date)
        res.update({'accrual_ids': accrual_ids})
        return res
