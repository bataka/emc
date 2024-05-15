from odoo import models, api, fields, _


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    driver_license_no = fields.Char()
    driver_license_date = fields.Date()
    driver_license_expired_date = fields.Date()
    driving_history_ids = fields.One2many("driving.history", "employee_id")


class DrivingHistory(models.Model):
    _name = "driving.history"
    _description = "Driving History"

    employee_id = fields.Many2one("hr.employee")
    vehicle_id = fields.Many2one("fleet.vehicle")
    reason = fields.Char()
    description = fields.Char()
    date = fields.Date()
