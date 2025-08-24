# -*- coding: utf-8 -*-
from odoo import api, fields, models


class KmPatient(models.Model):
    """Hospital patient."""

    _name = "km.patient"
    _description = "Patient"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "name"

    patient_code = fields.Char(string="Patient Code", copy=False, index=True, readonly=True)
    name = fields.Char(required=True, tracking=True)
    dob = fields.Date(string="Date of Birth")
    sex = fields.Selection([("m", "Male"), ("f", "Female"), ("o", "Other")])
    phone = fields.Char()
    department_id = fields.Many2one("km.department", string="Department")
    primary_doctor_id = fields.Many2one("km.doctor", string="Primary Doctor")
    allergies = fields.Text()
    notes = fields.Text()

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("patient_code"):
                vals["patient_code"] = self.env["ir.sequence"].next_by_code("km.patient") or "/"
        return super().create(vals_list)
