# -*- coding: utf-8 -*-
from odoo import fields, models


class KmDepartment(models.Model):
    """Hospital department."""

    _name = "km.department"
    _description = "Hospital Department"
    _order = "name"

    name = fields.Char(required=True)
    code = fields.Char()
    description = fields.Text()
    doctor_ids = fields.One2many("km.doctor", "department_id", string="Doctors")
    patient_ids = fields.One2many("km.patient", "department_id", string="Patients")
