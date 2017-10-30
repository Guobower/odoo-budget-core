# -*- coding: utf-8 -*-
{
    'name': "Budget Core",
    'version': '11.0.0.1',
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
- Budget Plan
- Project (Inherit to Budget)
- Project History (Inherit to Budget History)
- Project Plan (Inherit to Budget Plan)
- Cost Center - Account Code (Inherit to Budget)
- Cost Center - Account Code History (Inherit to Budget History)
- Cost Center - Account Code Plan (Inherit to Budget Plan)
- Access Users
    - Dependent - Can readonly
    - User - General Usage except delete power, can Edit plan but not create
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
        'security/ir.model.access.csv',
        'security/budget_access_rule.xml',

        # VIEWS
        'views/budget.xml',
        'views/budget_history.xml',
        'views/budget_plan.xml',
        'views/cost_center.xml',
        'views/account_code.xml',
        'views/account_code_area_spent.xml',
        'views/accrual.xml',
        'views/accrual_summary.xml',

        'views/rfq_inherit.xml',

        'views/budget_inherit_operation.xml',
        'views/budget_history_inherit_operation.xml',
        'views/budget_plan_inherit_operation.xml',

        'views/budget_inherit_project.xml',
        'views/budget_history_inherit_project.xml',
        'views/budget_plan_inherit_project.xml',

        'views/contract_inherit.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
