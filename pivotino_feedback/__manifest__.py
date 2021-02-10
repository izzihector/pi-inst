{
    'name': 'Pivotino Feedback Snackbar',
    'version': '13.0.1.0.0',
    'author': 'Onnet Consulting Sdn Bhd',
    'category': 'Tools',
    'description': """
Pivotino Feedback Snackbar
==========================
""",
    'website': 'https://on.net.my/',
    'depends': [
        'web',
        'pivotino_base'
    ],
    'data': [
        'data/feedback_cron.xml',
        'views/assets.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [],
    'qweb': [
        'views/feedback_snackbar.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}