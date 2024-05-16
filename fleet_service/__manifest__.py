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
        "data/report_actions.xml",
        "data/cron.xml",
        "data/mail_template.xml",
        "security/ir.model.access.csv",
        "views/employee_views.xml",
        "views/diagnosis_history_views.xml",
        "views/fleet_vehicle_views.xml",
        "wizard/diagnosis_history_bulk_changes_views.xml",
        "wizard/diagnosis_history_bulk_changes_v2_views.xml",
        "wizard/fleet_service_report_wizard_views.xml",
        "report/fleet_service_report_pdf.xml",
    ],
    # "installable": True
}
