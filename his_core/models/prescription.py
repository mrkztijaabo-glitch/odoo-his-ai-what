from odoo import models, fields

class HisPrescription(models.Model):
    _name = "his.prescription"
    _description = "Medication Order"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    patient_id = fields.Many2one("his.patient", required=True, ondelete="cascade")
    encounter_id = fields.Many2one("his.encounter", ondelete="set null")

    drug_name = fields.Char(required=True)
    dose = fields.Char(help="e.g., 500 mg")
    route = fields.Char(help="e.g., PO")
    frequency = fields.Char(help="e.g., BID")
    duration = fields.Char(help="e.g., 5 days")
    notes = fields.Text()
    status = fields.Selection(
        [("draft", "Draft"), ("active", "Active"), ("completed", "Completed"), ("stopped", "Stopped")],
        default="draft",
    )
