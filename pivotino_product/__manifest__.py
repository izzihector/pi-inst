{
    'name': 'Pivotino Product',
    'version': '13.0.1.0.0',
    'author': 'Onnet Consulting Sdn Bhd',
    'category': 'Hidden',
    'description': """
Pivotino Product
=================
    """,
    'website': 'https://on.net.my/',
    'depends': ['product', 'pivotino_base', 'web'],
    'data': [
        'views/pivotino_product_views.xml',
        'views/assets.xml',
        'data/pivotino_res_currency_data.xml',
        'views/res_partner_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'post_init_hook': '_change_currency_position'
}
