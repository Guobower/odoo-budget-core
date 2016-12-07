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

    def test_cc_ac(self):
        """
        test uniqueness of CC-AC
        """
        self.env['budget.core.budget'].create(
            {
                'cost_center_account_code': "PROJECT 1"
            }
        )

        with self.assertRaises(IntegrityError):
            self.env['budget.core.budget'].create(
                {
                    'cost_center_account_code': "PROJECT 1"
                }
            )