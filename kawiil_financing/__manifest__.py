{
    'name': "Kawiil Financing",
    'summary': "Simplifie le processus de demande de prêt pour les concessionnaires.",
    'category': "Kawiil/Custom Modules",
    'version': "1.0.0",
    'author': "Malick SENE/MalickSe",
    'depends': ['product'],

    'data': [
    'security/ir.model.access.csv',
    'views/loan_application_views.xml',
    'views/kawiil_financing_menu.xml',
    ],
    'demo': [
    'demo/loan_demo.xml',
    ],

    'license': "OPL-1",
    'application': True,
}
