{
    'name': "Kawiil Financing",
    'summary': "Simplifie le processus de demande de prêt pour les concessionnaires.",
    'category': "Kawiil/Custom Modules",
    'version': "1.0.0",
    'author': "Malick SENE/MalickSe",
    'depends': ['product'],
    'images': ['static/description/icon.png'],
    'data': [
    'security/categories.xml',
    'security/kawiil_financing_groups.xml',
    'security/ir.model.access.csv',
    'security/kawiil_financing_security.xml',
    'views/loan_application_views.xml',
    'views/kawiil_financing_menu.xml',
    'views/config_views.xml',
    'views/config_menu.xml',
    ],
    'demo': [
    'demo/config_demo.xml',
    'demo/loan_demo.xml',
    ],

    'license': "OPL-1",
    'application': True,
}
