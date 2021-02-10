{
    'name': 'Pivotino Web Responsive',
    'version': '13.0.1.0.0',
    'author': 'Onnet Consulting Sdn Bhd',
    'category': 'Tools',
    'description': """
Pivotino Web Responsive
=======================
""",
    'website': 'https://on.net.my/',
    'depends': [
        'ow_web_responsive',
    ],
    'data': [
        'views/assets.xml',
        'views/res_lang_views.xml',
        'views/res_users_views.xml',
        'views/res_partner_views.xml',
    ],
    'demo': [],
    'qweb': [
        'static/src/xml/apps.xml',
        'views/base_mobile.xml',
        'views/nav_footer.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
