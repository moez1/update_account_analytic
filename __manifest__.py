# -*- coding: utf-8 -*-
{
    'name': 'update account analytic',
    'version': '1.1',
    'category': 'account',
    'sequence': 35,
    'summary': 'entretien odoo',
    'author': 'Moez Labidi',
    'description': """
account analytic odoo
""",
    'website': '',
    'depends': ['account','account_accountant'],
    'data': [
        'wizard/entretien _odoo_view.xml',
        'views/account_invoice_view.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
