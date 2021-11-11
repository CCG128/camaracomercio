# -*- coding: utf-8 -*-
{
    'name': "Camara de comercio de Guatemala",

    'summary': """ Camara de comercio de Guatemala """,

    'description': """
         Módulo para Camara de comercio de Guatemala
    """,

    'author': "Aquih S.A.",
    'website': "http://www.aquih.com",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['account','product','contacts','purchase','event_sale','helpdesk'],

    'data': [
        'security/camaracomercio_security.xml',
        'views/product_template_views.xml',
        'views/product_views.xml',
        'views/purchase_views.xml',
        'views/camaracomercio_views.xml',
        'views/helpdesk_views.xml',
        'views/event_views.xml',
        'views/res_partner_view.xml',
        'views/account_view.xml',
        'security/ir.model.access.csv',
        'views/reporte_contrasenia.xml',
        'views/reporte_payment1.xml',
        'views/reporte_payment2.xml',
        'views/reporte_payment3.xml',
        'views/reporte_payment4.xml',
        'views/reporte_payment5.xml',
        'views/reporte_payment6.xml',
        'views/reporte_payment7.xml',
        'views/reporte_payment8.xml',
        'views/report.xml',
        'views/report_factura_electronica.xml',
    ],
}
