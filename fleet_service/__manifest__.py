# -*- coding: utf-8 -*-
{
    "name": "Fleet Service",
    "summary": "Short (1 phrase/line) summary of the module's purpose",
    "description": """
Long description of module's purpose
    """,
    "author": "Erdenet Mining Corporation",
    "website": "https://www.emc.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Uncategorized",
    "version": "0.1",
    # any module necessary for this one to work correctly
    "depends": ["fleet", "hr"],
    # always loaded
    "data": [
        "data/cron.xml",
        "data/mail_template.xml",
        "security/ir.model.access.csv",
        "views/employee_views.xml",
        "views/fleet_vehicle_views.xml",
    ],
    # "installable": True
}
