# -*- coding: utf-8 -*-
from odoo import http

# class /vagrant/odooModules/budgetCapex(http.Controller):
#     @http.route('//vagrant/odoo_modules/budget_capex//vagrant/odoo_modules/budget_capex/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('//vagrant/odoo_modules/budget_capex//vagrant/odoo_modules/budget_capex/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('/vagrant/odoo_modules/budget_capex.listing', {
#             'root': '//vagrant/odoo_modules/budget_capex//vagrant/odoo_modules/budget_capex',
#             'objects': http.request.env['/vagrant/odoo_modules/budget_capex./vagrant/odoo_modules/budget_capex'].search([]),
#         })

#     @http.route('//vagrant/odoo_modules/budget_capex//vagrant/odoo_modules/budget_capex/objects/<model("/vagrant/odoo_modules/budget_capex./vagrant/odoo_modules/budget_capex"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('/vagrant/odoo_modules/budget_capex.object', {
#             'object': obj
#         })