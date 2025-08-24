# -*- coding: utf-8 -*-
from odoo import fields, models


class KmDoctor(models.Model):
    """Medical doctor."""

    _name = "km.doctor"
    _description = "Doctor"
    _order = "name"

    name = fields.Char(required=True)
    code = fields.Char()
    department_id = fields.Many2one("km.department", string="Department")
    phone = fields.Char()
    email = fields.Char()
    active = fields.Boolean(default=True)
    patient_ids = fields.One2many("km.patient", "primary_doctor_id", string="Patients")
