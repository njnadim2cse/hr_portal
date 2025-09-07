{
    'name': 'HR Dashboard Updated',
    'version': '1.0',
    'summary': 'Custom HR Dashboard for Employees',
    'depends': ['hr', 'hr_attendance', 'web'],
    'data': [
        'views/dashboard_main.xml',
        'views/dashboard_attendance.xml',
        'views/leave_dashboard_template.xml',
        'views/loan_financial_aid.xml',
        'views/dashboard_expense.xml',
        'views/db_aboutme.xml',

    ],
    'application': True,
}
