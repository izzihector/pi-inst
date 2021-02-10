# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    "name": "Pivotino Branding",
    "summary": "",
    "version": "13.0.1.0.0",
    "category": "Hidden",
    "website": "https://www.pivotino.com",
    "author": "Pivotino",
    "license": "LGPL-3",
    "installable": True,
    "depends": [
        'auth_signup',
        'web_editor',
        'mail_bot',
        'web_unsplash',
    ],
    "data": [
        'views/webclient_templates.xml',
        'views/auth_signup_data.xml',
        'data/res_users_data.xml',
        'data/res_company_data.xml',
        'data/mailbot_data.xml',
        'views/assets.xml',
        'views/ir_module_views.xml',
        'views/res_config_settings_views.xml',
        'wizard/base_partner_merge_views.xml',
        'views/ir_ui_menu_views.xml',
        'views/res_company_views.xml',
        'views/res_partner_views.xml',
    ],
    'qweb': [
        'static/src/xml/wysiwyg.xml',
        'static/src/xml/discuss.xml',
        'static/src/xml/unsplash_image_widget.xml',
        'static/src/xml/base_import.xml'
    ],
}
