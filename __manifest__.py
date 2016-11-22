# -*- coding: utf-8 -*-
{
    'name': "Budget Core",
    'version': '0.1',
    'summary': 'Budget Core Module',
    'sequence': 1,
    'description': """
Odoo Module
===========
Specifically Designed for Etisalat-TBPC

Budget Core
---------------------
- Budget
- Project
- Cost Center - Account Code

    """,
    'author': "Marc Philippe de Villeres",
    'website': "https://github.com/mpdevilleres",
    'category': 'TBPC Budget',
    'depends': [
        'budget_enduser'
    ],
    'data': [
#        'security/budget.xml',
#        'security/ir.model.access.csv',

#        'views/task.xml',
       'views/budget.xml',
       'views/budget_inherit_project.xml',
       'views/menu.xml'
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
