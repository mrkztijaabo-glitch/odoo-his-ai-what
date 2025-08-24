# -*- coding: utf-8 -*-
from odoo import fields, models


class KmTest(models.Model):
    """Lab test definition."""

    _name = "km.test"
    _description = "Test"
    _order = "name"

    code = fields.Char()
    name = fields.Char(required=True)
    unit = fields.Char()
    ref_low = fields.Float(string="Ref. Low")
    ref_high = fields.Float(string="Ref. High")
    description = fields.Text()
