from odoo import models, fields, api

class HisPatient(models.Model):
    _name = "his.patient"
    _description = "Patient"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "display_name"

    # Basic demographics (expand later)
    first_name = fields.Char(required=True, tracking=True)
    last_name = fields.Char(required=True, tracking=True)
    date_of_birth = fields.Date(tracking=True)
    sex = fields.Selection(
        [("male", "Male"), ("female", "Female"), ("other", "Other")],
        tracking=True,
    )

    # Communication
    phone_e164 = fields.Char(string="Phone (E.164)", tracking=True)
    whatsapp_opt_in = fields.Boolean(default=False, tracking=True)
    preferred_language = fields.Selection(
        [("en", "English"), ("ar", "Arabic"), ("fr", "French")],
        default="en",
        tracking=True,
    )

    # Display
    display_name = fields.Char(compute="_compute_display_name", store=True)

    @api.depends("first_name", "last_name")
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"{rec.first_name or ''} {rec.last_name or ''}".strip()
