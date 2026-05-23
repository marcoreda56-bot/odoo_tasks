{
    'name': 'Hospitals Management System (HMS)',
    'author': 'Marco Reda',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/department_view.xml',
        'views/doctor_view.xml',
        'views/patient_view.xml',
    ],
    'installable': True,
    'application': True,
}