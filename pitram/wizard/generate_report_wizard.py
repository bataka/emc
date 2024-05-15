from odoo import models, fields, api, _


class GenerateReportWizard(models.TransientModel):
    _name = "generate.report.wizard"
    _description = "Generate Report Wizard"

    from_date = fields.Date()
    to_date = fields.Date()

    def pdf_export(self):
        print("####################")
        print("####################")
        print("####################")
        print("####################")
        data = {"from_date": self.from_date, "to_date": self.to_date}
        return self.env.ref("pitram.action_fleet_vehicle_report").report_action(
            self, data=data
        )
