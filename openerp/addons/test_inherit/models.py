# -*- coding: utf-8 -*-
from openerp import models, fields, api, osv


# We just create a new model
class mother(models.Model):
    _name = 'test.inherit.mother'

    _columns = {
        # check interoperability of field inheritance with old-style fields
        'name': osv.fields.char('Name'),
        'state': osv.fields.selection([('a', 'A'), ('b', 'B')], string='State'),
    }
    _defaults = {
        'name': 'Foo',
    }

    surname = fields.Char(compute='_compute_surname')

    @api.one
    @api.depends('name')
    def _compute_surname(self):
        self.surname = self.name or ''


# We want to inherits from the parent model and we add some fields
# in the child object
class daughter(models.Model):
    _name = 'test.inherit.daughter'

    template_id = fields.Many2one('test.inherit.mother', 'Template',
                                  delegate=True, required=True, ondelete='cascade')
    field_in_daughter = fields.Char('Field1')


# We add a new field in the parent object. Because of a recent refactoring,
# this feature was broken.
# This test and these models try to show the bug and fix it.
class mother(models.Model):
    _inherit = 'test.inherit.mother'

    field_in_mother = fields.Char()
    partner_id = fields.Many2one('res.partner')

    # extend the name field: make it required and change its default value
    name = fields.Char(required=True, default='Bar')

    # extend the selection of the state field
    state = fields.Selection(selection_add=[('c', 'C')])

    # override the computed field, and extend its dependencies
    @api.one
    @api.depends('field_in_mother')
    def _compute_surname(self):
        if self.field_in_mother:
            self.surname = self.field_in_mother
        else:
            super(mother, self)._compute_surname()


class mother(models.Model):
    _inherit = 'test.inherit.mother'

    # extend again the selection of the state field
    state = fields.Selection(selection_add=[('d', 'D')])


class daughter(models.Model):
    _inherit = 'test.inherit.daughter'

    # simply redeclare the field without adding any option
    template_id = fields.Many2one()

    # change the default value of an inherited field
    name = fields.Char(default='Baz')


class res_partner(models.Model):
    _inherit = 'res.partner'

    # define a one2many field based on the inherited field partner_id
    daughter_ids = fields.One2many('test.inherit.daughter', 'partner_id')


# Check the overriding of property fields by non-property fields.
# Contribution by Adrien Peiffer (ACSONE).
class test_inherit_property(models.Model):
    _name = 'test.inherit.property'

    _columns = {
        'name': osv.fields.char('Name', required=True),
        'property_foo': osv.fields.property(string='Foo', type='integer'),
        'property_bar': osv.fields.property(string='Bar', type='integer'),
    }


class test_inherit_property(models.Model):
    _inherit = 'test.inherit.property'

    @api.multi
    def _get_foo(self, name, arg):
        return dict.fromkeys(self.ids, 42)

    _columns = {
        # override property_foo with an old-api function field
        'property_foo': osv.fields.function(_get_foo, type='integer', string='Foo'),
    }

    # override property_bar with a new-api computed field
    property_bar = fields.Integer(compute='_compute_bar', company_dependent=False)

    @api.multi
    def _compute_bar(self):
        for record in self:
            record.property_bar = 42
