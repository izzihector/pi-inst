{
    'name': 'Pivotino CRM',
    'version': '12.0.1.0.0',
    'author': 'Onnet Consulting Sdn Bhd',
    'category': 'Hidden',
    'description': """
Pivotino CRM Customization
=============================
    """,
    'website': 'https://on.net.my/',
    'depends': ['sale_crm', 'pivotino_base', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'security/sale_target_security.xml',
        'views/res_company_views.xml',
        'views/pivotino_crm_stage_views.xml',
        'views/pivotino_crm_views.xml',
        'views/pivotino_crm_team_views.xml',
        'views/crm_lead_sequence.xml',
        'views/pivotino_lost_reason_views.xml',
        'views/pivotino_sale_target_views.xml',
        'views/webclient_templates.xml',
        'views/pivotino_sale_order_views.xml',
        'wizard/crm_lead_lost_quotation_views.xml',

        'data/analytic_tracking_data.xml',
        'data/pivotino_crm_lead_cron.xml',
        'data/pivotino_crm_stage_data.xml',
        'data/pivotino_crm_lost_data.xml',
        'data/pivotino_sale_target_cron.xml',
        'data/pivotino_crm_lead_sequence_data.xml',
        'data/pivotino_mail_activity.xml',
    ],
    'installable': True,
    'auto_install': False,
}
