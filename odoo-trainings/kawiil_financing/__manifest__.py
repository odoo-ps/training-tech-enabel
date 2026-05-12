{
    'name': 'Kawiil Financing',
    'summary': 'Streamlines the loan application process for dealerships.',
    'license': 'OPL-1',
    'category': 'Kawiil/Kawiil',
    'author': 'Odoo, Inc.',
    'website': 'https://github.com/odoo-trainings/kawiil-base/',
    'version': '1.0.1',
    'depends': ['product'],
    'data': [
        "security/kawiil_financing_groups.xml",
        "security/ir.model.access.csv",
        "security/kawiil_financing_security.xml",
        "views/loan_application_views.xml",
        "views/jawiil_financing_menu.xml",
    ],
    'demo': [
        "demo/loan_demo.xml",
    ],
    'application': True,
} 
