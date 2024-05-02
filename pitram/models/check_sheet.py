# -*- coding: utf-8 -*-

from odoo.exceptions import ValidationError, UserError
from odoo import models, fields, api, _


class CheckSheet(models.Model):
    _name = "check.sheet"
    _description = "Check Sheet"
    _rec_name = "sheet_num"

    license_no = fields.Char("License No", related="driver_id.license_no")
    sheet_num = fields.Char("Sheet Num", readonly=True)

    def action_confirm(self):
        if self.env.user.has_group('pitram.fleet_group_doctor'):
            self.state = "provided"
        else:
            raise UserError(_("You cant confirm"))

    def action_cancel(self):
        self.state = "draft"

    def action_create_task(self):
        self.env["check.sheet.task"].create(
            {
                "check_sheet_id": self.id,
                "customer": "-",
                "route": "{0} -> {1}".format(self.from_location, self.dest_location),
                "note": self.license_no,
            }
        )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals["sheet_num"] = self.env["ir.sequence"].next_by_code("check.sheet")

        return super().create(vals_list)

    vehicle_id = fields.Many2one(
        "fleet.vehicle",
        string="Vehicle",
        help="Fleet Vehicle Help",
        required=True,
        index=True,
    )
    driver_id = fields.Many2one(
        "res.partner",
        string="Driver",
    )
    from_location = fields.Char("From Location")
    dest_location = fields.Char("Destination Location")
    fuel_qty = fields.Float("Given Fuel Qty")
    distance = fields.Float("Distance km")
    state = fields.Selection(selection="_get_states", default="draft", string="State")
    sheet_date = fields.Date("Sheet date")
    start_odometer = fields.Integer(
        "Start odometer",
        help="Previous date consumed",
        compute="_compute_start_odometer",
        store=True,
    )
    end_odometer = fields.Integer("End Odometer")
    consumed_odometer = fields.Integer(
        "Consumed odometer", compute="_compute_consumed_odometer", store=True
    )
    vehicle_sheets = fields.One2many(
        "check.sheet", string="Vehicle sheets", compute="_compute_vehicle_sheets"
    )
    tasks = fields.One2many("check.sheet.task", "check_sheet_id", string="Tasks")

    @api.depends("vehicle_id")
    def _compute_vehicle_sheets(self):
        last_records = self.search(
            [("vehicle_id", "=", self.vehicle_id.id)],
            order="sheet_date desc",
            limit=5,
        )
        self.vehicle_sheets = last_records

    @api.depends("vehicle_id", "sheet_date")
    def _compute_start_odometer(self):
        for rec in self:
            if rec.sheet_date and rec.vehicle_id:
                last_record = self.search(
                    [
                        ("sheet_date", "<", rec.sheet_date),
                        ("vehicle_id", "=", rec.vehicle_id.id),
                    ],
                    order="sheet_date desc",
                    limit=1,
                )
                rec.start_odometer = last_record.end_odometer
            else:
                rec.start_odometer = 0

    @api.depends("end_odometer")
    def _compute_consumed_odometer(self):
        for rec in self:
            val = rec.end_odometer - rec.start_odometer
            if val < 0:
                raise ValidationError("Exception")
            rec.consumed_odometer = val

    def _get_states(self):
        return [("draft", "Draft"), ("provided", "Provided"), ("done", "Done")]
