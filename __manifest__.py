{
    'name': 'Hospitals Management System (HMS)',
    'version': '1.0',
    'summary': 'Manage hospital patients data',
    'category': 'Healthcare',
    'author': 'Marco Reda',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'patient_view.xml',
    ],
    'installable': True,
    'application': True,
}