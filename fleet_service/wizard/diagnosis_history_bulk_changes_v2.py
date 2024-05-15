from odoo import models, fields, api, _


class DiagnosisHistoryBulkChangesV2(models.TransientModel):
    _name = "diagnosis.history.bulk.changes.v2"
    _description = "Diagnosis History Bulk Change V2"

    from_template_id = fields.Many2one("diagnosis.history.template")
    line_ids = fields.One2many("diagnosis.history.bulk.changes.line.v2", "wizard_id")

    @api.model
    def default_get(self, fields):
        print("#######################")
        res = super(DiagnosisHistoryBulkChangesV2, self).default_get(fields)
        print("#######################")
        print(self.env.context)
        active_ids = self.env.context.get("active_ids")
        histories = self.env["diagnosis.history"].browse(active_ids)
        line_ids = []
        for history in histories:
            line_ids.append((0, 0, {"diagnosis_history_id": history.id}))

        print(line_ids)
        res["line_ids"] = line_ids
        return res

    def do_action(self):
        for rec in self:

            for line_id in rec.line_ids:
                template_lines = (
                    line_id.diagnosis_history_id.line_ids.template_id.mapped(
                        lambda obj: obj.id
                    )
                )
                update_vals = [(5, 0)]
                for to_line_id in rec.from_template_id.line_ids:
                    if to_line_id.id not in template_lines:
                        update_vals.append(
                            (
                                0,
                                0,
                                {
                                    "template_id": to_line_id.id,
                                    # "diagnosis_history_id": line_id.diagnosis_history_id.id,
                                    "name": to_line_id.name,
                                    "employee_id": to_line_id.employee_id.id,
                                    "total": to_line_id.total,
                                },
                            )
                        )
                print("#######################")
                print(update_vals)
                print(update_vals)
                print("#######################")
                line_id.diagnosis_history_id.write({"line_ids": update_vals})

            # self.env["diagnosis.history.line"].create(create_vals)


class DiagnosisHistoryBulkChangesLineV2(models.TransientModel):
    _name = "diagnosis.history.bulk.changes.line.v2"
    _description = "Diagnosis History Bulk Change Line V2"
    _rec_name = "diagnosis_history_id"

    wizard_id = fields.Many2one("diagnosis.history.bulk.changes.v2")
    diagnosis_history_id = fields.Many2one("diagnosis.history")
