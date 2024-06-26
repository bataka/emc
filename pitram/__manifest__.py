# -*- coding: utf-8 -*-
{
    'name': "pitram",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.emc.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['fleet'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/fleet_vehicle_views.xml',
        'views/res_partner_views.xml',
        'views/check_sheet_views.xml',
        'views/check_sheet_task_views.xml',
        'data/data.xml',
        'security/security.xml',
        'report/ir_actions_report_templates.xml',
        'report/ir_actions_report.xml',
    ],
    # "installable": True
}

