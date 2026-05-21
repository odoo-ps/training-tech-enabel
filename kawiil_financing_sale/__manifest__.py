{
    'name': 'Kawiil Financing Sale',
    'version': '19.0.1',
    'category': 'Kawill/Custom Modules',
    'summary': 'Intégration entre les devis de vente et les demandes de prêt Kawiil',
    'author': 'sdelbeke',
    'license': 'OPL-1',
    'depends': [
        'sale',
        'kawiil_financing',
    ],
    'application': False,
    'auto_install': True,
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_views.xml',
        'views/sale_order_views.xml',
    ],
}
