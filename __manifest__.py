# -*- coding: utf-8 -*-
{
    'name': "Budget Core",
    'version': '0.1b',
    'summary': 'Budget Core Module',
    'sequence': 1,
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
       'security/budget.xml',
       'security/ir.model.access.csv',

       'views/budget.xml',
       'views/budget_history.xml',
       # 'views/budget_inherit_project.xml',
       'views/menu.xml'
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
