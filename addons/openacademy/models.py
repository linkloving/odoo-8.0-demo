# -*- coding: utf-8 -*-

from openerp import models, fields, api

class openacademy(models.Model):
    _name = 'openacademy.openacademy'

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
