# -*- coding: utf-8 -*-
from odoo import api, fields, models

class HisEncounter(models.Model):
    _name = "his.encounter"
    _description = "HIS Encounter"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "encounter_datetime desc"

    name = fields.Char("Encounter #", readonly=True, copy=False, index=True)
    patient_id = fields.Many2one("his.patient", string="Patient", required=True, ondelete="cascade")
    encounter_datetime = fields.Datetime("Date & Time", default=fields.Datetime.now, required=True)
    chief_complaint = fields.Text("Chief Complaint", tracking=True)
    vitals_temp_c = fields.Float("Temperature (°C)")
    vitals_bp_systolic = fields.Integer("BP Systolic")
    vitals_bp_diastolic = fields.Integer("BP Diastolic")
    vitals_pulse = fields.Integer("Pulse")
    vitals_spo2 = fields.Integer("SpO₂ (%)")
    problems = fields.Text("Problems / Impression")
    state = fields.Selection([("draft","Draft"),("closed","Closed")], default="draft", tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("name"):
                vals["name"] = self.env["ir.sequence"].next_by_code("his.encounter") or "/"
        return super().create(vals_list)

    def action_close(self):
        for rec in self:
            rec.state = "closed"
