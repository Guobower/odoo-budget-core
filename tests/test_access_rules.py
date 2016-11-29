# -*- coding: utf-8 -*-
from faker import Faker

from odoo.exceptions import AccessError
from odoo.tests.common import TransactionCase

fake = Faker()


class AccessRuleTestCase(TransactionCase):
    at_install = False
    post_install = True

    def setUp(self):
        super(AccessRuleTestCase, self).setUp()

        # CREATE USERS WITH GROUP
        user = {
            u'lang': u'en_US',
            u'tz': False,
            u'notify_email': u'always',
            u'alias_contact': False,
            u'image': False,
            u'alias_id': False,
            u'company_id': 1,
            u'company_ids': [[6, False, [1]]],
            u'signature': u'',
            u'active': True,
            u'action_id': False
        }
        user.update(groups_id=[(6, 0, [self.env.ref('budget_core.group_budget_dependent').id])],
                    login=fake.safe_email(), email=fake.safe_email(), name=fake.name()
                    )
        self.budget_dependent = self.env['res.users'].create(user)

        user.update(groups_id=[(6, 0, [self.env.ref('budget_core.group_budget_user').id])],
                    login=fake.safe_email(), email=fake.safe_email(), name=fake.name()
                    )
        self.budget_user = self.env['res.users'].create(user)

        user.update(groups_id=[(6, 0, [self.env.ref('budget_core.group_budget_manager').id])],
                    login=fake.safe_email(), email=fake.safe_email(), name=fake.name()
                    )
        self.budget_manager = self.env['res.users'].create(user)

        user.update(groups_id=[(6, 0, [self.env.ref('budget_core.group_project_dependent').id])],
                    login=fake.safe_email(), email=fake.safe_email(), name=fake.name()
                    )
        self.project_dependent = self.env['res.users'].create(user)

        user.update(groups_id=[(6, 0, [self.env.ref('budget_core.group_project_user').id])],
                    login=fake.safe_email(), email=fake.safe_email(), name=fake.name()
                    )
        self.project_user = self.env['res.users'].create(user)

        user.update(groups_id=[(6, 0, [self.env.ref('budget_core.group_project_manager').id])],
                    login=fake.safe_email(), email=fake.safe_email(), name=fake.name()
                    )
        self.project_manager = self.env['res.users'].create(user)

        user.update(groups_id=[(6, 0, [self.env.ref('budget_core.group_operation_dependent').id])],
                    login=fake.safe_email(), email=fake.safe_email(), name=fake.name()
                    )
        self.operation_dependent = self.env['res.users'].create(user)

        user.update(groups_id=[(6, 0, [self.env.ref('budget_core.group_operation_user').id])],
                    login=fake.safe_email(), email=fake.safe_email(), name=fake.name()
                    )
        self.operation_user = self.env['res.users'].create(user)

        user.update(groups_id=[(6, 0, [self.env.ref('budget_core.group_operation_manager').id])],
                    login=fake.safe_email(), email=fake.safe_email(), name=fake.name()
                    )
        self.operation_manager = self.env['res.users'].create(user)

        # CREATE PROJECT, OPERATION

        self.project = self.env['budget.core.budget'].create(
            {
                u'is_project': True,
                u'name': u'project',
                u'initial_commitment_amount': 500,
                u'initial_expenditure_amount': 500,
                u'end_date': fake.date_time_this_month(before_now=True, after_now=False, tzinfo=None).strftime(
                    '%Y-%m-%d'),
                u'start_date': fake.date_time_this_month(before_now=False, after_now=True, tzinfo=None).strftime(
                    '%Y-%m-%d'),
                u'description': fake.text(max_nb_chars=200)
            }
        )

        self.operation = self.env['budget.core.budget'].create(
            {
                u'is_operation': True,
                u'name': u'operation',
                u'initial_expenditure_amount': 500,
                u'end_date': fake.date_time_this_month(before_now=True, after_now=False, tzinfo=None).strftime(
                    '%Y-%m-%d'),
                u'start_date': fake.date_time_this_month(before_now=False, after_now=True, tzinfo=None).strftime(
                    '%Y-%m-%d'),
                u'description': fake.text(max_nb_chars=200)
            }
        )

    def test_budget_dependent(self):
        """
        Can View All Budget
        Readonly
        """
        budgets = self.env['budget.core.budget'].sudo(self.budget_dependent).search([])

        # Check if project and operation is in budgets
        self.assertTrue(self.project in budgets, "Not All Budget row are visible")
        self.assertTrue(self.operation in budgets, "Not All Budget row are visible")

        # Tries to write but should fail
        with self.assertRaises(AccessError):
            budgets.write({u'name': 'test'})

    def test_budget_user(self):
        """
        Create but not Delete
        """
        budgets = self.env['budget.core.budget'].sudo(self.budget_user)
        budget = budgets.create(
            {
                u'name': u'project',
                u'initial_commitment_amount': 500,
                u'initial_expenditure_amount': 500,
                u'end_date': fake.date_time_this_month(before_now=True, after_now=False, tzinfo=None).strftime(
                    '%Y-%m-%d'),
                u'start_date': fake.date_time_this_month(before_now=False, after_now=True, tzinfo=None).strftime(
                    '%Y-%m-%d'),
                u'description': fake.text(max_nb_chars=200)
            }
        )
        self.assertTrue(budget in budgets.search([]), "budget not exist in Database")

        # Tries to write but should fail
        with self.assertRaises(AccessError):
            budgets.search([]).unlink()

    def test_budget_manager(self):
        """
        Can Delete
        """
        budgets = self.env['budget.core.budget'].sudo(self.budget_manager)

        budgets.search([]).unlink()

        self.assertTrue(len(budgets) == 0, "budgets not deleted")

    def test_project_access(self):
        """
        Must See Project Only
        """

        self.project = self.env['budget.core.budget'].create(
            {
                u'is_project': True,
                u'name': u'project',
                u'initial_commitment_amount': 500,
                u'initial_expenditure_amount': 500,
                u'end_date': fake.date_time_this_month(before_now=True, after_now=False, tzinfo=None).strftime(
                    '%Y-%m-%d'),
                u'start_date': fake.date_time_this_month(before_now=False, after_now=True, tzinfo=None).strftime(
                    '%Y-%m-%d'),
                u'description': fake.text(max_nb_chars=200)
            }
        )

        self.operation = self.env['budget.core.budget'].create(
            {
                u'is_operation': True,
                u'name': u'operation',
                u'initial_expenditure_amount': 500,
                u'end_date': fake.date_time_this_month(before_now=True, after_now=False, tzinfo=None).strftime(
                    '%Y-%m-%d'),
                u'start_date': fake.date_time_this_month(before_now=False, after_now=True, tzinfo=None).strftime(
                    '%Y-%m-%d'),
                u'description': fake.text(max_nb_chars=200)
            }
        )

        for access in [self.project_dependent, self.project_user, self.project_manager]:
            budgets = self.env['budget.core.budget'].sudo(access).search([])

            self.assertTrue(self.project in budgets, "Project is not visible in the budgets")
            self.assertTrue(self.operation not in budgets, "Operation is visible in the budgets")

    def test_operation_access(self):
        """
        Must See Operation Only
        """

        self.project = self.env['budget.core.budget'].create(
            {
                u'is_project': True,
                u'name': u'project',
                u'initial_commitment_amount': 500,
                u'initial_expenditure_amount': 500,
                u'end_date': fake.date_time_this_month(before_now=True, after_now=False, tzinfo=None).strftime(
                    '%Y-%m-%d'),
                u'start_date': fake.date_time_this_month(before_now=False, after_now=True, tzinfo=None).strftime(
                    '%Y-%m-%d'),
                u'description': fake.text(max_nb_chars=200)
            }
        )

        self.operation = self.env['budget.core.budget'].create(
            {
                u'is_operation': True,
                u'name': u'operation',
                u'initial_expenditure_amount': 500,
                u'end_date': fake.date_time_this_month(before_now=True, after_now=False, tzinfo=None).strftime(
                    '%Y-%m-%d'),
                u'start_date': fake.date_time_this_month(before_now=False, after_now=True, tzinfo=None).strftime(
                    '%Y-%m-%d'),
                u'description': fake.text(max_nb_chars=200)
            }
        )

        for access in [self.project_dependent, self.project_user, self.project_manager]:
            budgets = self.env['budget.core.budget'].sudo(access).search([])

            self.assertTrue(self.project in budgets, "Project is visible in the budgets")
            self.assertTrue(self.operation not in budgets, "Operation is not visible in the budgets")
