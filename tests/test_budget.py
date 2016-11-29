# -*- coding: utf-8 -*-
from psycopg2._psycopg import IntegrityError

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
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

    def test_update_history(self):
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

        history = self.env['budget.core.budget.history'].create(
            {
                'action_taken': 'transfer',
                'to_budget_id': budget.id,
                'from_budget_id': budget_b.id,
            }
        )

        self.assertTrue(history.budget_ids == budget + budget_b)

        history.write(
            {
                'from_budget_id': False,
            }
        )
        self.assertTrue(history.budget_ids == budget)

        history.write(
            {
                'from_budget_id': budget.id,
            }
        )
        self.assertTrue(history.budget_ids == budget)

        history.write(
            {
                'to_budget_id': budget_b.id,
                'from_budget_id': False,
            }
        )
        self.assertTrue(history.budget_ids == budget_b)

    def test_default_to_budget_id_create(self):
        """
        test default value of history.to_budget_id when creating budget
        """
        budget = self.env['budget.core.budget'].create(
            {
                u'name': u'budget_av',
                u'initial_expenditure_amount': 500,
                u'end_date': fake.date_time_this_month(before_now=True, after_now=False, tzinfo=None).strftime(
                    '%Y-%m-%d'),
                u'start_date': fake.date_time_this_month(before_now=False, after_now=True, tzinfo=None).strftime(
                    '%Y-%m-%d'),
                u'description': fake.text(max_nb_chars=200)
            }
        )
        self.assertTrue(budget.history_ids[0].to_budget_id == budget)

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

    def test_expenditure_amount_transfer(self):
        """
        test transfer validation for expenditure amount
        """
        budget = self.env['budget.core.budget'].create(
            {
                u'name': u'budget_av',
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
                u'name': u'budget_bv',
                u'initial_expenditure_amount': 1600,
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
                'expenditure_amount': 500,
                'action_taken': 'transfer',
                'from_budget_id': budget.id,
                'to_budget_id': budget_b.id,
            },
        ]
        # budget (0) ; budget_b (2100)
        budget.write({u'history_ids': [(0, 0, history) for history in histories]})
        self.assertTrue(budget.expenditure_amount == 0, "Budget A expenditure is %d" % budget.expenditure_amount)
        self.assertTrue(budget_b.expenditure_amount == 2100, "Budget B expenditure is %d" % budget_b.expenditure_amount)

        histories = [
            # Transfer Budget (1) to Budget_b
            {
                'expenditure_amount': 1,
                'action_taken': 'transfer',
                'from_budget_id': budget.id,
                'to_budget_id': budget_b.id,
            },
        ]
        # budget (-1) ; budget_b (2101)
        with self.assertRaises(ValidationError):
            budget.write({u'history_ids': [(0, 0, history) for history in histories]})

    def test_expenditure_amount_negative(self):
        """
        test negative validation for expenditure amount
        """
        budget = self.env['budget.core.budget'].create(
            {
                u'name': u'budget_av',
                u'initial_expenditure_amount': 500,
                u'end_date': fake.date_time_this_month(before_now=True, after_now=False, tzinfo=None).strftime(
                    '%Y-%m-%d'),
                u'start_date': fake.date_time_this_month(before_now=False, after_now=True, tzinfo=None).strftime(
                    '%Y-%m-%d'),
                u'description': fake.text(max_nb_chars=200)
            }
        )

        histories = [
            {
                'expenditure_amount': -500,
                'action_taken': 'add',
                'from_budget_id': budget.id,
            },
        ]
        # History expenditure is negative must raise ValidationError
        with self.assertRaises(IntegrityError):
            budget.write({u'history_ids': [(0, 0, history) for history in histories]})

    def test_recurrence_amount_negative(self):
        """
        test negative validation for recurrence amount
        """
        budget = self.env['budget.core.budget'].create(
            {
                u'name': u'budget_av',
                u'initial_expenditure_amount': 500,
                u'end_date': fake.date_time_this_month(before_now=True, after_now=False, tzinfo=None).strftime(
                    '%Y-%m-%d'),
                u'start_date': fake.date_time_this_month(before_now=False, after_now=True, tzinfo=None).strftime(
                    '%Y-%m-%d'),
                u'description': fake.text(max_nb_chars=200)
            }
        )

        recurrences = [
            {
                'recurrence_amount': -500,
            },
        ]
        # History expenditure is negative must raise IntegrityError
        with self.assertRaises(IntegrityError):
            budget.write({u'recurrence_ids': [(0, 0, recurrence) for recurrence in recurrences]})

    def test_workflow(self):
        """
        Test Workflow
        """
        budget = self.env['budget.core.budget'].create(
            {
                u'name': u'budget',
                u'initial_expenditure_amount': 500,
                u'end_date': fake.date_time_this_month(before_now=True, after_now=False, tzinfo=None).strftime(
                    '%Y-%m-%d'),
                u'start_date': fake.date_time_this_month(before_now=False, after_now=True, tzinfo=None).strftime(
                    '%Y-%m-%d'),
                u'description': fake.text(max_nb_chars=200)
            }
        )
        budget_a = self.env['budget.core.budget'].create(
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
                u'initial_expenditure_amount': 500,
                u'end_date': fake.date_time_this_month(before_now=True, after_now=False, tzinfo=None).strftime(
                    '%Y-%m-%d'),
                u'start_date': fake.date_time_this_month(before_now=False, after_now=True, tzinfo=None).strftime(
                    '%Y-%m-%d'),
                u'description': fake.text(max_nb_chars=200)
            }
        )

        budget_c = self.env['budget.core.budget'].create(
            {
                u'name': u'budget_c',
                u'initial_expenditure_amount': 500,
                u'end_date': fake.date_time_this_month(before_now=True, after_now=False, tzinfo=None).strftime(
                    '%Y-%m-%d'),
                u'start_date': fake.date_time_this_month(before_now=False, after_now=True, tzinfo=None).strftime(
                    '%Y-%m-%d'),
                u'description': fake.text(max_nb_chars=200)
            }
        )

        # INITIAL WORKFLOW DRAFT
        self.assertTrue(budget.state == 'draft')

        # DRAFT > ACTIVE
        budget.signal_workflow('active')
        self.assertTrue(budget.state == 'active')

        # ACTIVE > CLOSED
        budget.signal_workflow('close')
        self.assertTrue(budget.state == 'closed')

        # ALL TO CANCELLED
        budget_a.signal_workflow('cancel')
        self.assertTrue(budget_a.state == 'cancelled')

        budget_b.signal_workflow('active')
        budget_b.signal_workflow('cancel')
        self.assertTrue(budget_b.state == 'cancelled')

        # This Should fail because the flow ends also in close
        budget_c.signal_workflow('active')
        budget_c.signal_workflow('close')
        budget_c.signal_workflow('cancel')
        self.assertTrue(budget_c.state != 'cancelled')

        # Restart Process
