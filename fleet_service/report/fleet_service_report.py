from odoo import models, fields, api, _


class FleetServiceReportPDF(models.Model):
    _name = "report.fleet_service.fleet_service_report_pdf"

    def _get_report_values(self, docids, data=None):
        histories = self.env["diagnosis.history"].browse(
            data.get("context", {}).get("history_ids")
        )

        history_datas = []
        for h in histories:
            history_datas.append(
                {
                    "diagnosis_date": h.diagnosis_date,
                    "diagnosis_nex_date": h.diagnosis_nex_date,
                    "state": h.state,
                }
            )

        return {"history_datas": history_datas}
