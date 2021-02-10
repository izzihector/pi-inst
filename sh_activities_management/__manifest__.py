# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    'name': "Activities Management",
    'author' : 'Softhealer Technologies',
    'website': 'https://www.softhealer.com',
    "support": "support@softhealer.com",
    'category': 'CRM',
    'version': '13.0.1',
    "summary": """ Activity Management Odoo, Activity Scheduler Odoo, Manage Project Activity, Manage Employee Activity Module, Manage Supervisor Activity, Filter Completed Activity,filter planned Activity Odoo

                    """,
    'depends': ['crm','mail','web','pivotino_base'],
    'data': [
        'security/activity_security.xml',
        'views/activity_views.xml',
        'views/activity_dashboard.xml',
    ],
    'qweb': [
         'static/src/xml/activity_dashboard.xml'
    ],
    'images': ['static/description/background.png', ],
    "price": 100,
    "currency": "EUR"
}
