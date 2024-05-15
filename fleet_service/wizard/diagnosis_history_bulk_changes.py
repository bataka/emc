from odoo import models, fields, api, _


class DiagnosisHistoryBulkChanges(models.TransientModel):
    _name = "diagnosis.history.bulk.changes"
    _description = "Diagnosis History Bulk Change"

    template_id = fields.Many2one("diagnosis.history.template")
    from_template_id = fields.Many2one("diagnosis.history.template")
    line_ids = fields.One2many("diagnosis.history.bulk.changes.line", "wizard_id")

    @api.onchange("template_id")
    def _onchange_template_id(self):
        for rec in self:
            diagnosis_histories = self.env["diagnosis.history"].search(
                [("template_id", "=", rec.template_id.id)]
            )
            line_ids = []
            for obj in diagnosis_histories:
                line_ids.append((0, 0, {"diagnosis_history_id": obj.id}))

            rec.write({"line_ids": line_ids})

    def do_action(self):
        for rec in self:
            create_vals = []
            for line_id in rec.line_ids:
                template_lines = (
                    line_id.diagnosis_history_id.line_ids.template_id.mapped(
                        lambda obj: obj.id
                    )
                )

                for to_line_id in rec.from_template_id.line_ids:
                    if to_line_id.id not in template_lines:
                        create_vals.append(
                            {
                                "template_id": to_line_id.id,
                                "diagnosis_history_id": line_id.diagnosis_history_id.id,
                                "name": to_line_id.name,
                                "employee_id": to_line_id.employee_id.id,
                                "total": to_line_id.total,
                            }
                        )

            self.env["diagnosis.history.line"].create(create_vals)


class DiagnosisHistoryBulkChangesLine(models.TransientModel):
    _name = "diagnosis.history.bulk.changes.line"
    _description = "Diagnosis History Bulk Change Line"
    _rec_name = "diagnosis_history_id"

    wizard_id = fields.Many2one("diagnosis.history.bulk.changes")
    diagnosis_history_id = fields.Many2one("diagnosis.history")
