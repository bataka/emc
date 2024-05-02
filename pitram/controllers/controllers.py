# -*- coding: utf-8 -*-
# from odoo import http


# class Tender(http.Controller):
#     @http.route('/tender/tender', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tender/tender/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('tender.listing', {
#             'root': '/tender/tender',
#             'objects': http.request.env['tender.tender'].search([]),
#         })

#     @http.route('/tender/tender/objects/<model("tender.tender"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tender.object', {
#             'object': obj
#         })

