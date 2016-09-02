# -*- coding: utf-8 -*-

from datetime import timedelta
from openerp import models, fields, api, exceptions


# 其view层的展示在openacademy.xml
class Course(models.Model):
    # 该模型的名字
    _name = 'openacademy.course'

    '''
    string 是在UI上显示的标题 若不设置则默认为声明的变量（例如'description'）
    '''
    name = fields.Char(string="Title", required=True)

    description = fields.Text(string="description")

    # 一个责任人 有多个course
    responsible_id = fields.Many2one('res.users', ondelete='set null', string="teacher", index=True)

    # 一个course 有多个session
    session_ids = fields.One2many('openacademy.session', 'course_id', string="Sessions")

    # 在科目上方增加复制 因为name是（UNIQUE）
    # 我们需要把新复制的那么设置为 Copy of xxx
    @api.multi
    def copy(self, default=None):
        default = dict(default or {})

        copied_count = self.search_count(
            [('name', '=like', u"副本 {}%".format(self.name))])
        if not copied_count:
            new_name = u"副本 {}".format(self.name)
        else:
            new_name = u"副本 {} ({})".format(self.name, copied_count)
        default['name'] = new_name
        return super(Course, self).copy(default)

    # sql语句：name 和 description不能一样
    _sql_constraints = [
        ('name_description_check',
         'CHECK(name != description)',
         "The title of the course should not be the description"),
        # 设置name为 UNIQUE 唯一约束
        ('name_unique',
         'UNIQUE(name)',
         "The course title must be unique"),
    ]


# 课程表单
class Session(models.Model):
    _name = 'openacademy.session'

    name = fields.Char(string="Session Title", required=True)
    start_date = fields.Date(string="开课时间", )
    # digits(6 ,2) 共6位 小数点后只有2位
    duration = fields.Float(digits=(6, 2), help="Duration in days")

    seats = fields.Integer(string="座位数量")

    # active = fields.Boolean(default=True)

    # 每个session只能有一个Instructor                                      # 域
    instructor_id = fields.Many2one('res.partner', string="Instructor", domain=[('instructor', '=', True),
                                                                                ('category_id.name', 'ilike', "Teacher")])
    # 每个session只能有一个Course
    course_id = fields.Many2one('openacademy.course', ondelte='cadcade', string="科目", required=True)

    # 每个session有多个参与者 每个参与者也可以参加其他session
    attendee_ids = fields.Many2many('res.partner', string="参与者(学生)")

    taken_seats = fields.Float(string="Taken seats", compute='_taken_seats')

    end_date = fields.Date(string="End Date",
                           store=True,
                           compute='_get_end_date',
                           inverse='_set_end_date')

    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        for r in self:
            if not (r.start_date and r.duration):
                r.end_date = r.start_date
                continue

            # Add duration to start_date, but: Monday + 5 days = Saturday, so
            # subtract one second to get on Friday instead
            start = fields.Datetime.from_string(r.start_date)
            duration = timedelta(days=r.duration, seconds=-1)
            r.end_date = start + duration

    def _set_end_date(self):
        for r in self:
            if not (r.start_date and r.end_date):
                continue

            # Compute the difference between dates, but: Friday - Monday = 4 days,
            # so add one day to get 5 days instead
            start_date = fields.Datetime.from_string(r.start_date)
            end_date = fields.Datetime.from_string(r.end_date)
            r.duration = (end_date - start_date).days + 1

    @api.constrains('duration')
    def _check_dutarion_not_null(self):
        for r in self:
            if r.duration <=0.0 :
                raise exceptions.ValidationError('duration非法')

    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        for r in self:
            if not r.seats:
                r.taken_seats = 0.0
            else:
                print "输出r.attendee_ids:", len(r.attendee_ids)
                print "输出r.seats:", r.seats
                r.taken_seats = 100.0 * len(r.attendee_ids) / r.seats

    @api.onchange('seats', 'attendee_ids')
    def _verify_vaild_seats(self):
        if self.seats < 0:
            return {
                'warning':{
                    'title':'座位数有误',
                    'message':'座位数必须大于0',
                },
            }
        if self.seats < len(self.attendee_ids):
            return {
                'warning':{
                    'title':'座位数有误',
                    'message':'座位数小于学生数',
                },
            }

    @api.constrains('instructor_id', 'attendee_ids')
    def _check_instructor_not_in_attendes(self):
        for r in self:
            if r.instructor_id and r.instructor_id in r.attendee_ids:
                raise  exceptions.ValidationError('老师不能作为课程的学生')

    state = fields.Selection([
        ('draft', "草稿"),
        ('confirmed', "确认"),
        ('done', "完成")])

    @api.multi
    def action_draft(self):
        self.state = 'draft'

    @api.multi
    def action_confirm(self):
        self.state = 'confirmed'
        print '点击确认了 self.state：', self.state

    @api.multi
    def action_done(self):
        self.state = 'done'
