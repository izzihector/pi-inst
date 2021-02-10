{
    'name': 'Pivotino Auto Uninstall',
    'version': '13.0.1.0.0',
    'author': 'Onnet Consulting Sdn Bhd',
    'category': 'Hidden',
    'description': """
Pivotino Auto Uninstall Unnecessary Modules Upon Installing  
===========================================================
    """,
    'website': 'https://on.net.my/',
    'depends': [
        'pivotino_user_guide',
    ],
    'data': [],
    'auto_install': True,
    'post_init_hook': '_uninstall_modules',
}
