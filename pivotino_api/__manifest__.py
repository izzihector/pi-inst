{
    'name': 'Pivotino API',
    'version': '12.0.1.0.0',
    'author': 'Onnet Consulting Sdn Bhd',
    'category': 'Hidden',
    'description': """
Pivotino API Customization
=============================
    """,
    'website': 'https://on.net.my/',
    'depends': ['pivotino_base'],
    'data': [
        'security/ir.model.access.csv',

        'data/api_configuration_data.xml',

        'views/api_configuration_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
