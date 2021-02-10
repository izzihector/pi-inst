{
    'name': 'Pivotino Pre-Configuration',
    'version': '12.0.1.0.0',
    'author': 'Onnet Consulting Sdn Bhd',
    'category': 'Hidden',
    'description': """
Pivotino Pre-Configuration Customization
===========================================
    """,
    'website': 'https://on.net.my/',
    'depends': ['pivotino_crm', 'ks_dashboard_ninja', 'web', 'pivotino_api'],
    'data': [
        'data/analytic_tracking_data.xml',
        'security/ir.model.access.csv',

        'views/res_users.xml',

        'wizard/pivotino_first_time_login_wizard_views.xml',
        'wizard/starter_wizard_view.xml',
        'static/src/xml/base.xml',
    ],
    'installable': True,
    'auto_install': False,
}
