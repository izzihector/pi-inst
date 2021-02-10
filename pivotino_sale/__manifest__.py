{
    'name': 'Pivotino Sale',
    'version': '13.0.1.0.0',
    'author': 'Onnet Consulting Sdn Bhd',
    'category': 'Hidden',
    'description': """
Pivotino Sale
==============
    """,
    'website': 'https://on.net.my/',
    'depends': ['sale_management', 'pivotino_base'],
    'data': [
        'data/sale_data.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/pivotino_sale_views.xml',
        'views/res_partner_views.xml',
        'views/res_currency_views.xml',
        'views/account_tax_views.xml',
    ],
    'installable': True,
    'auto_install': False,
}
