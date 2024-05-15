from psycopg2 import sql

from odoo import tools
from odoo import models, fields, api, _


class FleetReport(models.Model):
    _name = "fleet.report"
    _description = "Fleet Report"
    _auto = False

    driver_id = fields.Many2one("res.partner")
    future_driver_id = fields.Many2one("res.partner")

    def init(self):
        query = """
            SELECT
                rp.id AS driver_id,
                rpf.id AS future_driver_id
            FROM
                fleet_vehicle fh
                LEFT JOIN res_partner rp ON rp.id = fh.driver_id
                LEFT JOIN res_partner rpf ON rpf.id = fh.future_driver_id
        """
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(
            sql.SQL("""CREATE or REPLACE VIEW {} as ({})""").format(
                sql.Identifier(self._table), sql.SQL(query)
            )
        )
