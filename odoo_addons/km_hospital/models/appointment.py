# -*- coding: utf-8 -*-
from odoo import api, fields, models


class KmAppointment(models.Model):
    """Patient appointment."""

    _name = "km.appointment"
    _description = "Appointment"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "datetime_start desc"

    name = fields.Char(readonly=True, copy=False, index=True)
    patient_id = fields.Many2one("km.patient", string="Patient", required=True)
    doctor_id = fields.Many2one("km.doctor", string="Doctor", required=True)
    department_id = fields.Many2one(
        "km.department", string="Department", compute="_compute_department_id", store=True
    )
    datetime_start = fields.Datetime(string="Start", default=fields.Datetime.now, required=True)
    reason = fields.Text()
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("scheduled", "Scheduled"),
            ("done", "Done"),
            ("cancelled", "Cancelled"),
        ],
        default="draft",
        tracking=True,
    )

    @api.depends("doctor_id")
    def _compute_department_id(self):
        for rec in self:
            rec.department_id = rec.doctor_id.department_id

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("name"):
                vals["name"] = self.env["ir.sequence"].next_by_code("km.appointment") or "/"
        return super().create(vals_list)

    def action_confirm(self):
        for rec in self:
            rec.state = "scheduled"

    def action_done(self):
        for rec in self:
            rec.state = "done"

    def action_cancel(self):
        for rec in self:
            rec.state = "cancelled"
