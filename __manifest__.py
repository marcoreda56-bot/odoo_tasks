{
    'name': 'Hospitals Management System (HMS)',
    'author': 'Marco Reda',
    'depends': ['base', 'crm'],
    'data': [
        'security/ir.model.access.csv',
        'views/department_view.xml',
        'views/doctor_view.xml',
        'views/patient_view.xml',
        'views/customer_view.xml',
    ],
    'installable': True,
    'application': True,
}