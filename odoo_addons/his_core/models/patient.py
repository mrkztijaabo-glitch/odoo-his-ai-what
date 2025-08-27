from odoo import models, fields

class Patient(models.Model):
    _name = 'his.patient'
    _description = 'Patient'

    name = fields.Char(string='Name', required=True, tracking=True)
    phone = fields.Char(string='Phone', required=True, tracking=True)
