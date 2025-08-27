from odoo import models, fields

class HisEncounter(models.Model):
    _name = "his.encounter"
    _description = "Clinical Encounter"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    patient_id = fields.Many2one("his.patient", required=True, ondelete="cascade")
    start_datetime = fields.Datetime(default=fields.Datetime.now, required=True)
    end_datetime = fields.Datetime()
    chief_complaint = fields.Char(tracking=True)
    notes = fields.Text()

    # simple vitals to start
    height_cm = fields.Float()
    weight_kg = fields.Float()
    temperature_c = fields.Float()
    systolic_bp = fields.Integer()
    diastolic_bp = fields.Integer()
