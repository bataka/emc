from odoo import models, fields, api, _


class FleetServiceReport(models.Model):
    _name = "fleet.service.report"
    _description = "Fleet Service Report"

    name = fields.Char()
