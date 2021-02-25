# -*- coding: utf-8 -*-
{
    'name': "Smart trading late",

    'summary': """
       Late Attendece Approval """,

    'description': """
       Late Attendece Approval
    """,

    'author': "Codeso",
    'website': "https://codeso.lk",
    'license':'Other proprietary',
    'category': 'Employees',
    'version': '1.0.0',
    'depends': ['hr_contract','hr_attendance','hr','hr_payroll', 'hr_holidays'],
    'data': [
        'views/codeso_late.xml',
        'data/late_schedule.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}