# -*- coding: utf-8 -*-

from odoo.exceptions import ValidationError
from odoo import models, fields, api


class CheckSheetTask(models.Model):
    _name = "check.sheet.task"
    _description = "Check Sheet Task"

    check_sheet_id = fields.Many2one(
        "check.sheet",
        string="Check Sheet",
        required=True,
        index=True,
    )
    customer = fields.Char("Customer")
    route = fields.Char("Route")
    note = fields.Char("Note")
