# -*- coding: utf-8 -*-
{
    'name': "Budget Core",
    'version': '0.2',
    'summary': 'Budget Core Module',
    'sequence': 3,
    'description': """
Budget Core
===========
Specifically Designed for Etisalat-TBPC

Summary
---------------------
- Budget
- Budget History
- Budget Recurrence
- Project (Inherit to Budget)
- Project History (Inherit to Budget History)
- Project Recurrence (Inherit to Budget Recurrence)
- Cost Center - Account Code (Inherit to Budget)
- Cost Center History (Inherit to Budget History)
- Cost Center Recurrence (Inherit to Budget Recurrence)
- Access Users
    - Budget (View All)
        - Dependent - Can readonly
        - User - General Usage except delete power, can Edit recurrence but not create
        - Manager - All power to manipulate data
    - Project
        - Dependent - Can readonly
        - User - General Usage except delete power, can Edit recurrence but not create
        - Manager - All power to manipulate data
    - Cost Center
        - Dependent - Can readonly
        - User - General Usage except delete power, can Edit recurrence but not create
        - Manager - All power to manipulate data
- Validations
    - Project
        - Project Expenditure Amount Can't be More Than Commitment Amount
        - When Transferring Expenditure/Commitment Amount, the losing amount shouldn't be negative after the operation
        - When Adding/Subtracting Expenditure/Commitment Amount, the losing amount shouldn't be negative after the operation
        - Project No must be unique
        - Recurring Amounts should be Positive
    - Cost Center - Account Code
        - When Transferring Expenditure, the losing amount shouldn't be negative after the operation
        - When Adding/Subtracting Expenditure, the losing amount shouldn't be negative after the operation
        - Cost Center - Account Code must be unique
        - Recurring Amounts should be Positive
- Utilities
    """,
    'author': "Marc Philippe de Villeres",
    'website': "https://github.com/mpdevilleres",
    'category': 'TBPC Budget',
    'depends': [
        'budget_enduser',
        'budget_contractor'
    ],
    'data': [
        # SECURITY
        'security/budget.xml',
        'security/budget_access_rule.xml',
        'security/ir.model.access.csv',

        # VIEWS
        'views/budget.xml',
        'views/budget_history.xml',
        'views/budget_recurrence.xml',
        'views/cost_center.xml',
        'views/account_code.xml',

        'views/budget_inherit_operation.xml',
        'views/budget_history_inherit_operation.xml',
        'views/budget_recurrence_inherit_operation.xml',

        'views/budget_inherit_project.xml',
        'views/budget_history_inherit_project.xml',
        'views/budget_recurrence_inherit_project.xml',

        'views/contract_inherit.xml',

        'views/menu.xml',

        # WORKFLOWS
        'workflows/budget_core_budget.xml'

    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
