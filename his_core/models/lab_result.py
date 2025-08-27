from odoo import models, fields

class HisLabResult(models.Model):
    _name = "his.lab.result"
    _description = "Lab Result"
    _inherit = ["mail.thread"]

    patient_id = fields.Many2one("his.patient", required=True, ondelete="cascade")
    encounter_id = fields.Many2one("his.encounter", ondelete="set null")

    # Minimal LOINC-like fields (you can load codes later)
    test_code = fields.Char(required=True, help="LOINC or local code")
    test_name = fields.Char(required=True)
    value = fields.Char()
    unit = fields.Char()
    reference_range = fields.Char()
    status = fields.Selection(
        [("prelim", "Preliminary"), ("final", "Final"), ("corrected", "Corrected")],
        default="prelim",
    )
    observed_at = fields.Datetime(default=fields.Datetime.now)
