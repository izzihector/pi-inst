{
    'name': 'Pivotino Base',
    'version': '12.0.1.0.0',
    'author': 'Onnet Consulting Sdn Bhd',
    'category': 'Hidden',
    'description': """
Pivotino Base Customization
=============================
    """,
    'website': 'https://on.net.my/',
    'depends': ['base', 'mail'],
    'data': [
        'security/base_security.xml',
        'security/pivotino_security.xml',
        'security/ir.model.access.csv',

        'data/analytic_tracking_data.xml',
        'data/pivotino_industry_data.xml',
        'data/pivotino_parameter.xml',
        'data/res_users_data.xml',
        'data/res_partner_data.xml',
        'data/cron.xml',
        'data/res_lang_data.xml',

        'views/res_company_views.xml',
        'views/res_partner_views.xml',
        'views/res_users_views.xml',
        'views/base_menus.xml',

        'wizard/pivotino_password_wizard_views.xml',
    ],
    'installable': True,
    'auto_install': False,
}
