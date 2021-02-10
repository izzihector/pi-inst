{
    'name': 'Pivotino Instance Status',
    'version': '13.0.1.0.0',
    'author': 'Onnet Consulting Sdn Bhd',
    'category': 'Hidden',
    'description': """
Pivotino Instance Status Check Portal Checkbox to Notify Instance Provision
===========================================================================
    """,
    'website': 'https://on.net.my/',
    'depends': [
        'pivotino_api'
    ],
    'data': [],
    'auto_install': False,
    'post_init_hook': '_check_instance_status',
}
