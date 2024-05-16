from odoo import models, fields, api, _


class FleetServiceReportPDF(models.AbstractModel):
    _name = "report.fleet_service.fleet_service_report_pdf"

    def _get_report_values(self, docids, data=None):
        histories = self.env["diagnosis.history"].browse(data.get("history_ids"))

        print("#################")
        print(data.get("context", {}))
        print(histories)
        print("#################")

        history_datas = []
        for h in histories:
            history_datas.append(
                {
                    "diagnosis_date": h.diagnosis_date,
                    "diagnosis_next_date": h.diagnosis_next_date,
                    "state": h.state,
                }
            )

        return {
            "o": histories,
            "company": self.env.company,
            "history_datas": history_datas,
        }
