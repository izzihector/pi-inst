{
    'name': 'Pivotino Account',
    'version': '13.0.1.0.0',
    'author': 'Onnet Consulting Sdn Bhd',
    'category': 'Hidden',
    'description': """
Pivotino Account Customization
==============================
    """,
    'website': 'https://on.net.my/',
    'depends': ['account', 'pivotino_base'],
    'data': [
        'views/account_views.xml',
        'views/pivotino_product_views.xml',
        'views/partner_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
