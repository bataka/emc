# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class FleetController(http.Controller):

    @http.route("/fleet/", auth="public")
    def index(self, *args, **kwargs):
        return {"message": "Hello, world"}

    @http.route("/fleet/withlogin/", methods=["post"], type="json", auth="user")
    def withlogin(self, *args, **kwargs):
        # methods : POST, GET, PUT, DELETE, OPTION
        # type : http, json
        # auth : user, public, none
        # cors : True
        # csrf : True
        print("################")
        print(args)
        print(kwargs)
        print(kwargs["send"])
        print(kwargs["send"])
        print(kwargs["send"])
        print(kwargs["send"])
        fleets = request.env["fleet.vehicle"].search([])
        print(fleets)
        print("################")
        return {"success": True}
