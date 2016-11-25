# -*- coding: utf-8 -*-
from openerp import http, fields
import json

class Data(http.Controller):
    @http.route('/compute_task_costs/', type='http', auth='public', methods=['POST'])
    def compute_task_cost(self, **post):
        pass

    @http.route('/count_project_cost/', type='http', auth='public', methods=['POST'])
    def count_project_cost(self, **post):
        project_cost = post['project_cost']
        project_cost = json.loads(project_cost)
        if project_cost:
            for project_cost in project_cost:
                pass
            for ids in range(0, len(project_cost['works'])):
                task_costs = project_cost['works']
                if task_costs[ids]:
                    work_id = task_costs[ids]
                    work_id['cost'] = 0
                    hr_costs = http.request.env['human_resource_cost.hr_cost'].sudo().search([('employee_id.work_email', '=', work_id['user_email'])])
                    work_date = fields.Date.from_string(work_id['date'])
                    for hr_cost in hr_costs:
                        hr_cost_date = fields.Date.from_string(hr_cost.date)
                        if hr_cost_date.month == work_date.month and hr_cost_date.year == work_date.year:
                            work_id['cost'] = (hr_cost.cost_day / 4) * work_id['hours']
            return json.dumps(project_cost['works'])
        else:
            return 0
    @http.route('/compute_all_cost/', type='http', auth='public', methods=['POST'])
    def compute_project_cost(self, **post):
        pass