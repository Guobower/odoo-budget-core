# -*- coding: utf-8 -*-
from psycopg2._psycopg import IntegrityError
from odoo.exceptions import ValidationError

from odoo.tests.common import TransactionCase

from faker import Faker
import random

fake = Faker()


class ProjectTestCase(TransactionCase):
    at_install = False
    post_install = True

    def setUp(self):
        super(ProjectTestCase, self).setUp()

    def test_commitment_amount(self):
        """
        commitment_amount is a compute field
        sum of all histories commitment amount
        """
        budget = self.env['budget.core.budget'].create(
            {
                u'is_project': True,
                u'name': u'budget_a',
                u'initial_commitment_amount': 500,
                u'end_date': fake.date_time_this_month(before_now=True, after_now=False, tzinfo=None).strftime(
                    '%Y-%m-%d'),
                u'start_date': fake.date_time_this_month(before_now=False, after_now=True, tzinfo=None).strftime(
                    '%Y-%m-%d'),
                u'description': fake.text(max_nb_chars=200)
            }
        )

        budget_b = self.env['budget.core.budget'].create(
            {
                u'is_project': True,
                u'name': u'budget_b',
                u'initial_commitment_amount': 1600,
                u'end_date': fake.date_time_this_month(before_now=True, after_now=False, tzinfo=None).strftime(
                    '%Y-%m-%d'),
                u'start_date': fake.date_time_this_month(before_now=False, after_now=True, tzinfo=None).strftime(
                    '%Y-%m-%d'),
                u'description': fake.text(max_nb_chars=200)
            }
        )

        # 'add', 'subtract', 'transfer'
        # 500(initial) + 1100 - 1000 + 1000 - 1000 + 1000(Transfer)
        histories = [
            {
                'commitment_amount': 1100,
                'action_taken': 'add'
            },
            {
                'commitment_amount': 1000,
                'action_taken': 'subtract'
            },
            {
                'commitment_amount': 1000,
                'action_taken': 'add'
            },
            {
                'commitment_amount': 1000,
                'action_taken': 'subtract'
            },
            {
                'commitment_amount': 1000,
                'action_taken': 'transfer',
                'to_budget_id': budget.id,
                'from_budget_id': budget_b.id,
            },
        ]

        budget.write({u'history_ids': [(0, 0, history) for history in histories]})

        self.assertTrue(budget.commitment_amount == 1600, "Budget A commitment is %d" % budget.commitment_amount)
        self.assertTrue(budget_b.commitment_amount == 600, "Budgt B commitment is %d" % budget_b.commitment_amount)

        # make new transfer from budget to budget_b
        self.env['budget.core.budget.history'].create(
            {
                'commitment_amount': 100,
                'action_taken': 'transfer',
                'to_budget_id': budget_b.id,
                'from_budget_id': budget.id,
            }
        )

        self.assertTrue(budget.commitment_amount == 1500, "Budget A commitment is %d" % budget.commitment_amount)
        self.assertTrue(budget_b.commitment_amount == 700, "Budgt B commitment is %d" % budget_b.commitment_amount)

    def test_commitment_amount_negative(self):
        """
        test negative validation for commitment amount
        """
        budget = self.env['budget.core.budget'].create(
            {
                u'is_project': True,
                u'name': u'budget_av',
                u'initial_commitment_amount': 500,
                u'end_date': fake.date_time_this_month(before_now=True, after_now=False, tzinfo=None).strftime(
                    '%Y-%m-%d'),
                u'start_date': fake.date_time_this_month(before_now=False, after_now=True, tzinfo=None).strftime(
                    '%Y-%m-%d'),
                u'description': fake.text(max_nb_chars=200)
            }
        )

        histories = [
            {
                'commitment_amount': -500,
                'action_taken': 'add',
                'from_budget_id': budget.id,
            },
        ]
        # History commitment is negative must raise ValidationError
        with self.assertRaises(IntegrityError):
            budget.write({u'history_ids': [(0, 0, history) for history in histories]})

    def test_commitment_amount_transfer(self):
        """
        test transfer validation for commitment amount
        """
        budget = self.env['budget.core.budget'].create(
            {
                u'is_project': True,
                u'name': u'budget_av',
                u'initial_commitment_amount': 500,
                u'end_date': fake.date_time_this_month(before_now=True, after_now=False, tzinfo=None).strftime(
                    '%Y-%m-%d'),
                u'start_date': fake.date_time_this_month(before_now=False, after_now=True, tzinfo=None).strftime(
                    '%Y-%m-%d'),
                u'description': fake.text(max_nb_chars=200)
            }
        )

        budget_b = self.env['budget.core.budget'].create(
            {
                u'is_project': True,
                u'name': u'budget_bv',
                u'initial_commitment_amount': 1600,
                u'end_date': fake.date_time_this_month(before_now=True, after_now=False, tzinfo=None).strftime(
                    '%Y-%m-%d'),
                u'start_date': fake.date_time_this_month(before_now=False, after_now=True, tzinfo=None).strftime(
                    '%Y-%m-%d'),
                u'description': fake.text(max_nb_chars=200)
            }
        )

        histories = [
            # Transfer Budget (500) to Budget_b
            {
                'commitment_amount': 500,
                'action_taken': 'transfer',
                'from_budget_id': budget.id,
                'to_budget_id': budget_b.id,
            },
        ]
        # budget (0) ; budget_b (2100)
        budget.write({u'history_ids': [(0, 0, history) for history in histories]})
        self.assertTrue(budget.commitment_amount == 0, "Budget A commitment is %d" % budget.commitment_amount)
        self.assertTrue(budget_b.commitment_amount == 2100, "Budget B commitment is %d" % budget_b.commitment_amount)

        histories = [
            # Transfer Budget (1) to Budget_b
            {
                'commitment_amount': 1,
                'action_taken': 'transfer',
                'from_budget_id': budget.id,
                'to_budget_id': budget_b.id,
            },
        ]
        # budget (-1) ; budget_b (2101)
        with self.assertRaises(ValidationError):
            budget.write({u'history_ids': [(0, 0, history) for history in histories]})

