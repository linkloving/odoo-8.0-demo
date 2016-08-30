# -*- coding: utf-8 -*-

from openerp import models, fields, api


# 提供给demo.xml设置属性
class Course(models.Model):
    _name = 'openacademy.course'
    '''
    string 是在UI上显示的标题 若不设置则默认为声明的变量（例如'description'）
    '''
    name = fields.Char(string="标题", required=True,help="请输入标题")
    description = fields.Text(string="描述")
