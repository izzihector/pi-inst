{
    'name': 'Pivotino Mobile Certification Customization',
    'version': '13.0.1.0.0',
    'author': 'Onnet Consulting Sdn Bhd',
    'category': 'Tools',
    'description': """
Pivotino Mobile Certification Customization
===========================================
""",
    'website': 'https://on.net.my/',
    'depends': [
        'pivotino_web_responsive',
    ],
    'data': [
        'views/webclient_templates.xml',
        'views/sale_order_views.xml',
        'views/res_partner_views.xml',
    ],
    'demo': [],
    'qweb': [
        'static/src/xml/base.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
