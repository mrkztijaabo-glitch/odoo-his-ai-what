# -*- coding: utf-8 -*-
from odoo import api, fields, models


class KmTestResult(models.Model):
    """Result of a lab test."""

    _name = "km.test.result"
    _description = "Test Result"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "create_date desc"

    appointment_id = fields.Many2one("km.appointment", string="Appointment", required=True)
    patient_id = fields.Many2one("km.patient", string="Patient", required=True, default=lambda self: self._default_patient())
    test_id = fields.Many2one("km.test", string="Test", required=True)
    value = fields.Float()
    unit = fields.Char()
    status = fields.Selection(
        [("draft", "Draft"), ("verified", "Verified")], default="draft", tracking=True
    )

    def _default_patient(self):
        appointment = self.env["km.appointment"].browse(self.env.context.get("default_appointment_id"))
        return appointment.patient_id

    @api.onchange("appointment_id")
    def _onchange_appointment_id(self):
        self.patient_id = self.appointment_id.patient_id

    @api.onchange("test_id")
    def _onchange_test_id(self):
        self.unit = self.test_id.unit

    def action_verify(self):
        for rec in self:
            rec.status = "verified"
