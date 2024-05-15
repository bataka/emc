from datetime import timedelta
from odoo import models, fields, api, _


# class Tax(models.Model):
#     pass


class FleetVehicle(models.Model):
    _inherit = "fleet.vehicle"

    diagnosis_history_ids = fields.One2many("diagnosis.history", "vehicle_id")

    @api.onchange("diagnosis_history_ids")
    def _onchange_diagnosis_history_ids(self):
        for rec in self:
            print("#############################")
            print("#############################")
            print("#############################")
            print("#############################")


class DiagnosisHistoryTemplate(models.Model):
    _name = "diagnosis.history.template"
    _description = "Diagnosis History Template"

    model_id = fields.Many2one("fleet.vehicle.model")
    line_ids = fields.One2many("diagnosis.history.line.template", "template_id")


class DiagnosisHistoryLineTemplate(models.Model):
    _name = "diagnosis.history.line.template"
    _description = "Diagnosis History Line Template"

    template_id = fields.Many2one("diagnosis.history.template")
    name = fields.Char()
    employee_id = fields.Many2one("hr.employee")
    total = fields.Integer(default=0)
    assessment = fields.Integer(default=0)


class DiagnosisHistory(models.Model):
    _name = "diagnosis.history"
    _description = "Diagnosis History"

    vehicle_id = fields.Many2one("fleet.vehicle")
    diagnosis_date = fields.Date()
    diagnosis_next_date = fields.Date(readonly=True)
    total = fields.Integer(compute="_compute_total")
    assessment = fields.Integer(compute="_compute_assessment")
    state = fields.Selection(
        [("draft", _("Draft")), ("pass", _("Pass")), ("fail", _("Fail"))],
        readonly=True,
    )
    line_ids = fields.One2many("diagnosis.history.line", "diagnosis_history_id")

    def onchange(self, values, field_names, fields_spec):

        print("###############")
        print("###############")
        print(self.id)
        print(self.id)
        vehicle_id = values.get("vehicle_id", {}).get("id")

        if vehicle_id:
            vehicle_obj_id = self.env["fleet.vehicle"].browse(vehicle_id)

            template_ids = self.env["diagnosis.history.template"].search(
                [("model_id", "=", vehicle_obj_id.model_id.id)]
            )

            if template_ids:
                template_id = template_ids[0]
                line_ids = []
                for template_line_id in template_id.line_ids:
                    line_ids.append(
                        (
                            0,
                            0,
                            {
                                "name": template_line_id.name,
                                "employee_id": template_line_id.employee_id.id,
                                "total": template_line_id.total,
                            },
                        )
                    )

                print(line_ids)
                print("##################")
                values.update({"line_ids": line_ids})

                self.line_ids = line_ids

        return super().onchange(values, field_names, fields_spec)

    @api.depends("line_ids")
    def _compute_total(self):
        for rec in self:
            # Example code
            # total = 0
            # for line_id in self.line_ids:
            #     total += line_id.total

            # def return_total(obj):
            #     return obj.total

            # rec.total = sum(self.line_ids.filtered(lambda obj: obj.total))
            # rec.total = sum(self.line_ids.recude(lambda obj: obj.total))
            rec.total = sum(self.line_ids.mapped(lambda obj: obj.total))

    @api.depends("line_ids")
    def _compute_assessment(self):
        for rec in self:
            rec.assessment = sum(self.line_ids.mapped(lambda obj: obj.assessment))

    @api.onchange("diagnosis_date")
    def _onchange_diagnosis_date(self):
        for rec in self:
            if rec.diagnosis_date:
                rec.diagnosis_next_date = rec.diagnosis_date + timedelta(days=365)
                rec.state = "draft"

    def approve(self):
        for rec in self:
            rec.state = "pass"

    def fail(self):
        for rec in self:
            rec.state = "fail"

    def run_diagnosis_alert(self):
        histories = self.env["diagnosis.history"].search([("state", "=", "pass")])
        print("######################")
        print(histories)
        print("######################")
        for history in histories:
            print(history.vehicle_id.driver_id.email)
            histories.action_send_and_print()

    def action_send_and_print(self):
        print("run template")
        template = self.env.ref(
            "fleet_service.email_template_diagnosis_alert", raise_if_not_found=False
        )

        template.sudo().send_mail(self.ids[0], force_send=True)

        template_id = self.env.ref("fleet_service.email_template_diagnosis_alert").id
        template = self.env["mail.template"].browse(template_id)
        template.send_mail(self.id, force_send=True)

        print(template)

        print("send template")
        return {
            "name": _("Send"),
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "diagnosis.history",
            "target": "new",
            "context": {
                "active_ids": self.ids,
                "default_mail_template_id": template and template.id or False,
            },
        }

    def _get_report_base_filename(self):
        return "Fleet Service Vehicle"


class DiagnosisHistoryLine(models.Model):
    _name = "diagnosis.history.line"
    _description = "Diagnosis History Line"

    diagnosis_history_id = fields.Many2one("diagnosis.history")
    name = fields.Char()
    employee_id = fields.Many2one("hr.employee")
    total = fields.Integer(default=0)
    assessment = fields.Integer(default=0)