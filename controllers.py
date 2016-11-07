# -*- coding: utf-8 -*-
from openerp import http

class Academy(http.Controller):
    @http.route('/academy/', auth='public', website=True)
    def index(self):
        m = http.request.env['academy.teachers']
        return http.request.render('academy.index2',
                                   {'teachers': m.search([]),}
                                   )
        '''
        return http.request.render('academy.index2', {
            'teachers': ["Diana Padilla1", "Jody Caroll3", "Lester Vaughn5"],
        })'''

    @http.route('/academy/<model("academy.teachers"):teacher>/', auth='public', website=True)
    def teacher(self, teacher):
        return http.request.render('academy.biography', {'person': teacher})


    #@http.route ('/firewell/', auth ='public',website=True)
    @http.route('/firewell/', auth ='public',website = True)
    def index1(self):

        m = http.request.env['academy.teachers']
        '''return http.request.render('academy.index',
                                   {'teachers': m.search([]),}
                                   )
        return http.request.render('academy.index', {
            'teachers': ["Diana Padilla1", "Jody Caroll3", "Lester Vaughn5"],
        })'''
        return '''
[

  {

    "date_modified": "Fri, 03 Jun 2016 09:13:08 -0000",

    "fw_ip": "1.1.252.1",

    "fw_name": "TEST-FW01"

  },

  {

    "date_modified": "Fri, 03 Jun 2016 09:13:08 -0000",

    "fw_ip": "1.1.252.200",

    "fw_name": "TEST-FW02"

  }

]
'''

'''
    @http.route('/academy/<name>/', auth='public', website=True)
    def teacher(self, name):
        return '<h1>{}</h1>'.format(name)
    @http.route('/academy/<int:id>/', auth='public', website=True)
    def teacher(self, id):
        return '<h1>{} ({})</h1>'.format(id, type(id).__name__)

'''

