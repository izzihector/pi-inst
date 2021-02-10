{
    "name": "Pivotino Branding Payment",
    "summary": "",
    "version": "13.0.1.0.0",
    "category": "Hidden",
    "website": "https://www.pivotino.com",
    "author": "Pivotino",
    "license": "LGPL-3",
    "installable": True,
    "depends": [
        'payment',
        'payment_paypal',
    ],
    "data": [
        'views/pivotino_payment_views.xml',
        'views/pivotino_payment_acquirer_onboarding_templates.xml',
    ],
    "qweb": [
        'static/src/xml/pivotino_payment_processing.xml',
    ],
}
