# -*- coding: utf-8 -*-

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
