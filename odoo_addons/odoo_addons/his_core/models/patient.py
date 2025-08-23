# -*- coding: utf-8 -*-
from odoo import api, fields, models

class HisPatient(models.Model):
    _name = "his.patient"
    _description = "HIS Patient"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "name"

    name = fields.Char("Full Name", required=True, tracking=True)
    patient_code = fields.Char("Patient ID", copy=False, index=True)
    dob = fields.Date("Date of Birth")
    sex = fields.Selection([("m", "Male"), ("f", "Female"), ("o", "Other")], string="Sex")
    phone_mobile_e164 = fields.Char("Mobile (E.164)")
    whatsapp_opt_in = fields.Boolean("WhatsApp Opt-in", default=False)
    preferred_language = fields.Selection(
        [("so_SO", "Somali"), ("en_US", "English"), ("ar_AR", "Arabic")],
        string="Preferred Language", default="so_SO",
    )
    quiet_hours = fields.Char("Quiet Hours (e.g. 21:00-07:00)")
    notes = fields.Text()

    _sql_constraints = [
        ("patient_code_unique", "unique(patient_code)", "Patient ID must be unique."),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("patient_code"):
                vals["patient_code"] = self.env["ir.sequence"].next_by_code("his.patient") or "/"
        return super().create(vals_list)
