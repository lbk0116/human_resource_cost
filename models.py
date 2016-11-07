# -*- coding: utf-8 -*-
from openerp import fields
from openerp import models,api
import datetime
DATE_FORMAT = "%Y-%m"


class hr_wages(models.Model):
    _name = 'humen_resource_cost.hr_wages'

    name  = fields.Char(string="姓名")
    monthly_wages = fields.Float(string="月工资")  # 月工资
    work_email = fields.Char(string="南天邮箱")

    project_subsidy = fields.Float(string="项目补贴")  # 项目补贴
    special_benefit = fields.Float(string="特殊补贴")  # 特殊补贴
    other_allowance = fields.Float(string="其它补贴")  # 其它补贴
    housing_fund = fields.Float(string="住房公积金")  # 住房公积金
    endowment_insurance = fields.Float(string="养老保险")  # 养老保险
    unemployment_insurance = fields.Float(string="失业保险")  # 失业保险
    medical_insurance = fields.Float(string="医疗保险")  # 医疗保险
    maternity_insurance = fields.Float(string="生育保险")  # 生育保险
    employment_injury_insurance = fields.Float(string="工伤保险")  # 工伤保险
    three_funds = fields.Float(string="三项经费")  # 三项经费
    department_alaverage_amortization = fields.Float(string="部门平均摊销")  # 部门平均摊销
    asset_depreciation_allocation = fields.Float(string="资产折旧分摊")  # 资产折旧分摊

    department_first =fields.Char(string ="一级部门")
    department_second = fields.Char(string="二级部门")
    department_third = fields.Char(string="三级部门")

    cost_coefficient = fields.Float(string="费用系数",default = 1)  # 费用系数
    sum = fields.Float(string="以上费用总计",store =True, compute='_get_total_cost')

    @api.depends('project_subsidy', 'special_benefit', 'other_allowance','housing_fund', 'endowment_insurance',\
                 'unemployment_insurance', 'medical_insurance', 'maternity_insurance', 'employment_injury_insurance',\
                 'three_funds', 'department_alaverage_amortization', 'asset_depreciation_allocation',"reimbursement_ids")
    def _get_total_cost(self):
        for record in self:
            record.sum = record.project_subsidy + record.special_benefit + record.other_allowance \
                           + record.housing_fund + record.endowment_insurance + record.unemployment_insurance \
                           + record.medical_insurance + record.maternity_insurance + record.employment_injury_insurance\
                           + record.three_funds + record.department_alaverage_amortization \
                           + record.asset_depreciation_allocation


    hr_cost_ids = fields.One2many('humen_resource_cost.hr_cost','employee_id',ondelete = 'set null',string="成本表")
    #cost = fields.Float(string="费用按照(0.5天计算)",related = "hr_cost_ids.cost")#这个cost要显示最后一个即本月的费用,得处理一下
    reimbursement_ids =fields.One2many('humen_resource_cost.reimbursement','employee_id',ondelete = 'set null',string="报销表")
    #监听这个字段,如果这个字段又出现了本表的ID,本字段就变化

    # 此条字段是为了便于显示
    cost_day = fields.Float(string="费用按照(0.5天计算)", store=True, compute='_get_data_cost')
    @api.depends('hr_cost_ids')
    def _get_data_cost(self):
        for x in self:
            if x.hr_cost_ids:
                x.cost_day = x.hr_cost_ids[-1].cost_day


    #test = fields.Char(string="测试字段")

class hr_cost(models.Model):
    _name ='humen_resource_cost.hr_cost'

    date = fields.Date(string="月份")
    monthly_wage_s= fields.Float(string="月工资")  # 月工资
    monthly_fee_for_service = fields.Float(store =True, compute='_get_pay_sum',string="月度实报实销",ondelete='set null')  # 月度实报实销
    cost_coefficient = fields.Float(string="费用系数", default=1)  # 费用系数
    cost_day = fields.Float(string="费用按照(0.5天计算)",store=True,compute='_get_date_cost')
    cost_month = fields.Float(string="费用按照(月计算)", store=True, compute='_get_date_cost')
    employee_id = fields.Many2one('humen_resource_cost.hr_wages',ondelete='set null',string="员工")
    reimbursement_ids = fields.One2many('humen_resource_cost.reimbursement',"hr_cost_id",ondelete='set null',string="报销表",store =True)

    department_first = fields.Char(string="一级部门")
    department_second = fields.Char(string="二级部门")
    department_third = fields.Char(string="三级部门")

    test = fields.Char(string="测试字段")

    @api.multi
    @api.depends('reimbursement_ids')
    def _get_pay_sum(self):
        for record in self:
            # print "每一条成本表"
            if len(record.reimbursement_ids):
            #如果报销表已经关联上
                for reimbursement_id in record.reimbursement_ids:
                    #print '每一条报销表'
                    if record.date and reimbursement_id.date:
                        date_reim = fields.Date.from_string(record.date)
                        date_cost = fields.Date.from_string(reimbursement_id.date)
                        if date_reim.month == date_cost.month:
                            #计算所有实报实销
                            record.monthly_fee_for_service += reimbursement_id.pay
                    else:
                        pass
            else:
                record.test = "报销表不存在或未关联"

    #这里要实现一个安排动作,每月创建一次下个月的的成本表
    @api.multi
    def make_cost_list(self):
        #print '这里要实现一个安排动作,每天检测工资表里的日期,如果'
        now = fields.datetime.now()
        #print now.day
        recs = self.env['humen_resource_cost.hr_wages'].search([])
        for rec in recs:
            exist = 0
            strs = self.env['humen_resource_cost.hr_cost'].search([("employee_id", "=", rec.id)])
            # print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
            for str in strs:
                #print str.date.year,str.date.month
                st = fields.Date.from_string(str.date)
                if st.year == now.year and st.month == now.month:
                    # print st.year,st.month
                    exist = 1
                    break
            if exist==1:
                continue
            id = self.env['humen_resource_cost.hr_cost'].create({'employee_id': rec.id,'monthly_wage_s':rec.monthly_wages,'date':now,"cost_coefficient":rec.cost_coefficient,\
                                                                "department_first":rec.department_first,"department_second":rec.department_second,"department_third":rec.department_third})
            if not id.date:
                print "成本表时间创建不成功"


    #总计整个月的实报实销
    @api.multi
    @api.depends('reimbursement_ids')
    def total_monthly_fee_for_service(self):
        for m in self:
            for n in m.reimbursement_ids:
                m.monthly_fee_for_service +=n.pay



    @api.depends('employee_id.sum','monthly_wage_s','monthly_fee_for_service','cost_coefficient')
    def _get_date_cost(self):
        for record in self:
            record.cost_month = (record.employee_id.sum+record.monthly_wage_s+record.monthly_fee_for_service)* record.cost_coefficient
            record.cost_day = (record.cost_month/ 21.5) * 0.5


class reimbursement(models.Model):
    _name = 'humen_resource_cost.reimbursement'

    name = fields.Char(string="姓名")
    work_mail  = fields.Char(string="南天邮箱")
    #name = fields.Char(related='hr_cost_id.employee_id', string="报销人")
    department = fields.Char(string = "报销部门")
    date = fields.Date(string = "报销日期")
    kinds = fields.Char(string = "费用种类")
    project = fields.Char(string = "项目名称")
    pay = fields.Float(string = "报销金额")
    hr_cost_id = fields.Many2one('humen_resource_cost.hr_cost', ondelete='set null', string="工资单",store =True,compute = "reimbursement_match_hr_cost")
    employee_id = fields.Many2one('humen_resource_cost.hr_wages',ondelete='set null', string="报销人",store = True, compute = "reimbursement_match_employee")

    test = fields.Char(string="数据状态")

    #报销表导入就触动函数与人员表关联
    #ID不能触动
    @api.depends('work_mail')
    @api.multi
    def reimbursement_match_employee(self):
        for rec in self:
            ress = self.env['humen_resource_cost.hr_wages'].search([("work_email",'=',rec.work_mail)])
            if ress:
                rec.employee_id = ress.id
                rec.test = '已关联到人员'
            else:
                rec.test = '未关联到人员'
                print rec.test

    #报销和人员表关联之后,将报销表与成本表关联
    @api.multi
    @api.depends('employee_id','date')
    def reimbursement_match_hr_cost(self):
        for count in self:
            if count.employee_id:
                if count.date:
                    date_reim = fields.Datetime.from_string(count.date)
                    ress = self.env['humen_resource_cost.hr_cost'].search([("employee_id", "=", count.employee_id.id)])
                    for res in ress:
                        if res.date:
                            date_cost = fields.Datetime.from_string(res.date)
                            #应该只有一个月份符合if条件
                            if date_reim.month == date_cost.month:
                            #把成本表的ID存到报销表下,即关联起来
                                # print date_reim.month
                                # print date_cost.month
                                count.hr_cost_id = res.id
                                count.test = "已关联到成本"
                                break
                            else:
                                # print date_reim.month
                                # print date_cost.month
                                # #count.hr_cost_id = ''
                                count.test = "未匹配到时间"
                        else:
                            res.test = "成本时间不合格"
                else:
                    count.test = '报销时间不合格'
            else :
                count.test = '未关联到人员'



            # else:
            #     count.test = "报销和人员表仍没关联上"
            #     print count.test






