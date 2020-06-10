# -*- coding: utf-8 -*-
from odoo import http

# class Rooms(http.Controller):
#     @http.route('/rooms/rooms/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rooms/rooms/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('rooms.listing', {
#             'root': '/rooms/rooms',
#             'objects': http.request.env['rooms.rooms'].search([]),
#         })

#     @http.route('/rooms/rooms/objects/<model("rooms.rooms"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rooms.object', {
#             'object': obj
#         })