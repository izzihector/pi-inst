{
    'name': 'Pivotino Mail',
    'version': '13.0.1.0.0',
    'author': 'Onnet Consulting Sdn Bhd',
    'category': 'Hidden',
    'description': """
Pivotino Mail Customization
===========================
    """,
    'website': 'https://on.net.my/',
    'depends': ['mail', 'pivotino_base'],
    'data': [
        'data/analytic_tracking_data.xml',
        'wizard/mail_feedback_wizard_view.xml',
        'views/activity_quick_access_menu.xml',
        'views/activity_views.xml',
        'views/mail_views.xml',
    ],
    'qweb': [
        'static/src/xml/activity_quick_access_menu.xml'
    ],
    'installable': True,
    'auto_install': False,
}