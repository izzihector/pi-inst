{
    'name': 'Pivotino General Feedback',
    'version': '13.0.1.0.0',
    'author': 'Onnet Consulting Sdn Bhd',
    'category': 'Tools',
    'description': """
Pivotino General Feedback
===========================
""",
    'website': 'https://on.net.my/',
    'depends': [
        'web',
        'pivotino_base',
    ],
    'data': [
        'data/feedback_cron.xml',
        'data/feedback_tags_data.xml',

        'security/ir.model.access.csv',

        'views/assets.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
