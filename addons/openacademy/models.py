# -*- coding: utf-8 -*-

from openerp import models, fields, api


# 其view层的展示在openacademy.xml
class Course(models.Model):
    _name = 'openacademy.course'
    '''
    string 是在UI上显示的标题 若不设置则默认为声明的变量（例如'description'）
    '''
    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="description")
    # 一个责任人 有多个course
    responsible_id = fields.Many2one('res.user', ondelete='set null', string="责任人", index=True)
    # 一个course 有多个session
    session_ids = fields.One2many('openacademy.session', 'course_id', string="Sessions")


# 会议表单
class Session(models.Model):
    _name = 'openacademy.session'

    name = fields.Char(string="Session Title", required=True)
    start_data = fields.Date()
    # digits(6 ,2) 共6位 小数点后只有2位
    duration = fields.Float(digits=(6, 2), help="Duration in days")
    seats = fields.Integer(string="座位号")
    # 每个session只能有一个Instructor
    instructor_id = fields.Many2one('res.partner', string="Instructor")
    # 每个session只能有一个Course
    course_id = fields.Many2one('openacademy.course', ondelte='cadcade', string="Course", required=True)
    # 每个session只能有多个参与者 每个参与者也可以参加其他session
    attendee_ids = fields.Many2many('res.partner', string="参与者")
