# -*- coding: utf-8 -*-
{
    'name': "Budget Core",
    'version': '0.1b',
    'summary': 'Budget Core Module',
    'sequence': 2,
    'description': """
Odoo Module
===========
Specifically Designed for Etisalat-TBPC

Budget Core
---------------------
- Budget
- Budget History
- Project (Inherit to Budget)
- Project History (Inherit to Budget History)
- Cost Center - Account Code (Inherit to Budget)
- Cost Center History (Inherit to Budget History)
- Access Users
    - Dependent - Can readonly
    - User - General Usage except delete power
    - Manager - All power to manipulate data
- Utilities

Brief
---------------------
    """,
    'author': "Marc Philippe de Villeres",
    'website': "https://github.com/mpdevilleres",
    'category': 'TBPC Budget',
    'depends': [
        'budget_enduser'
    ],
    'data': [
        # SECURITY
        'security/budget.xml',
        'security/ir.model.access.csv',

        # VIEWS
        'views/budget.xml',
        'views/budget_history.xml',
        'views/budget_inherit_operation.xml',
        'views/budget_history_inherit_operation.xml',
        'views/budget_inherit_project.xml',
        'views/budget_history_inherit_project.xml',
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
