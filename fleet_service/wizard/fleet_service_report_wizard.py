from odoo import models, fields, api, _


class FleetServiceReportWizard(models.TransientModel):
    _name = "fleet.service.report.wizard"
    _description = "Fleet Service Report Wizard"

    from_date = fields.Date()
    to_date = fields.Date()
    group_by = fields.Selection(
        [
            ("date", _("Date")),
            ("vehicle", _("Vehicle")),
        ]
    )
    vehicle_ids = fields.Many2many("fleet.vehicle")

    def export_pdf(self):
        from_date = self.from_date
        to_date = self.to_date
        vehicle_ids = self.vehicle_ids
        group_by = self.group_by

        domain = [
            ("diagnosis_date", ">=", from_date),
            ("diagnosis_date", "<", to_date),
        ]

        if vehicle_ids:
            domain.append(("vehicle_id", "in", vehicle_ids.ids))

        histories = self.env["diagnosis.history"].search(domain)

        data = {"history_ids": histories.ids, "group_by": group_by}

        return self.env.ref(
            "fleet_service.action_fleet_service_report_pdf"
        ).report_action(self, data=data)

    def export_excel(self):
        pass
