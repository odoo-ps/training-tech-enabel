{
    'name': 'Kawiil Financing',
    'version': '19.0.0',
    'category': 'Kawill/Custom Modules',
    'summary': 'Simplifie le processus de demande de prêt pour les concessionnaires',
    'author': 'sdelbeke',
    'license': 'OPL-1',
    'depends': [
        'product'
    ],
    'application': True,
    'data': [
        'security/kawiil_financing_groups.xml',
        'security/ir.model.access.csv',
        'security/kawiil_financing_security.xml',
        'views/loan_application_views.xml',
        'views/loan_application_tag_views.xml',
        'views/loan_application_document_type_views.xml',
        'views/kawiil_financing_menu.xml',
    ],
    'demo': [
        'demo/config_demo.xml',
        'demo/loan_demo.xml',
    ],
}
