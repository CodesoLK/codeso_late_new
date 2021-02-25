# -*- coding: utf-8 -*-
from flectra import http

# class CodesoOvertime(http.Controller):
#     @http.route('/codeso_overtime/codeso_overtime/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/codeso_overtime/codeso_overtime/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('codeso_overtime.listing', {
#             'root': '/codeso_overtime/codeso_overtime',
#             'objects': http.request.env['codeso_overtime.codeso_overtime'].search([]),
#         })

#     @http.route('/codeso_overtime/codeso_overtime/objects/<model("codeso_overtime.codeso_overtime"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('codeso_overtime.object', {
#             'object': obj
#         })