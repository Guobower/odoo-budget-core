# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase

from faker import Faker
import random

fake = Faker()


class BudgetTestCase(TransactionCase):
    at_install = False
    post_install = True

    def setUp(self):
        super(BudgetTestCase, self).setUp()

    def test_initial_history(self):
        """
        Checks if initial history created
        """

        # create random budget
        for i in range(1, 5):
            budget = self.env['budget.core.budget'].create(
                {
                    u'name': u'budget_%d' % i,
                    u'initial_expenditure_amount': random.uniform(10000.00, 99999.99),
                    u'end_date': fake.date_time_this_month(before_now=True, after_now=False, tzinfo=None).strftime(
                        '%Y-%m-%d'),
                    # u'section_id': False,
                    # u'sub_section_id': False,
                    # u'state': u'draft',
                    # u'write_date': False,
                    # u'history_ids': [],
                    u'start_date': fake.date_time_this_month(before_now=False, after_now=True, tzinfo=None).strftime(
                        '%Y-%m-%d'),
                    u'description': fake.text(max_nb_chars=200)
                }
            )

            self.assertTrue(len(budget.history_ids) == 1, "History must be 1 only at initial create")

    def test_expenditure_amount(self):
        """
        expenditure_amount is a compute field
        sum of all histories expenditure amount
        """
        budget = self.env['budget.core.budget'].create(
            {
                u'name': u'budget_a',
                u'initial_expenditure_amount': 500,
                u'end_date': fake.date_time_this_month(before_now=True, after_now=False, tzinfo=None).strftime(
                    '%Y-%m-%d'),
                u'start_date': fake.date_time_this_month(before_now=False, after_now=True, tzinfo=None).strftime(
                    '%Y-%m-%d'),
                u'description': fake.text(max_nb_chars=200)
            }
        )

        budget_b = self.env['budget.core.budget'].create(
            {
                u'name': u'budget_b',
                u'initial_expenditure_amount': 1600,
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
                'expenditure_amount': 1100,
                'action_taken': 'add'
            },
            {
                'expenditure_amount': 1000,
                'action_taken': 'subtract'
            },
            {
                'expenditure_amount': 1000,
                'action_taken': 'add'
            },
            {
                'expenditure_amount': 1000,
                'action_taken': 'subtract'
            },
            {
                'expenditure_amount': 1000,
                'action_taken': 'transfer',
                'to_budget_id': budget.id,
                'from_budget_id': budget_b.id,
            },
        ]

        budget.write({u'history_ids': [(0, 0, history) for history in histories]})

        self.assertTrue(budget.expenditure_amount == 1600, "Budget A expenditure is %d" % budget.expenditure_amount)
        self.assertTrue(budget_b.expenditure_amount == 600, "Budgt B expenditure is %d" % budget_b.expenditure_amount)

        # make new transfer from budget to budget_b
        self.env['budget.core.budget.history'].create(
            {
                'expenditure_amount': 100,
                'action_taken': 'transfer',
                'to_budget_id': budget_b.id,
                'from_budget_id': budget.id,
            }
        )

        self.assertTrue(budget.expenditure_amount == 1500, "Budget A expenditure is %d" % budget.expenditure_amount)
        self.assertTrue(budget_b.expenditure_amount == 700, "Budgt B expenditure is %d" % budget_b.expenditure_amount)

    # TRANSISTION TESTS
    # ----------------------------------------------------------

    def test_set2draft(self):
        pass

    #        self.state = 'draft'


    def test_set2active(self):
        pass

    #        self.state = 'active'


    def test_set2close(self):
        pass
        #        self.state = 'closed'
