{
    'name': 'Pivotino User Guide',
    'version': '13.0.1.0.0',
    'author': 'Anonymous',
    'category': 'Hidden',
    'description': """
Pivotino User Guide
===================
""",
    'website': 'https://www.pivotino.com/',
    'depends': ['web_tour', 'mail', 'pivotino_pre_config'],
    'data': [
        'data/analytic_tracking_data.xml',
        'security/ir.model.access.csv',
        'views/templates.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'installable': True,
    'auto_install': True,
}
