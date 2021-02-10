{
    'name': 'Pivotino Mobile',
    'version': '13.0.1.0.0',
    'author': 'Anonymous',
    'category': 'Hidden',
    'description': """
Pivotino Mobile
===============
""",
    'website': 'https://www.pivotino.com/',
    'depends': ['web', 'pivotino_base'],
    'data': [
        'views/templates.xml',
    ],
    'qweb': [
        "static/src/xml/*.xml",
    ],
    'installable': True,
    'auto_install': True,
}
