# -*- coding: utf-8 -*-
{
    "name": "HIS Core",
    "version": "16.0.1.0.0",
    "license": "LGPL-3",
    "category": "Healthcare",
    "summary": "Core patient management model",
    "depends": ["base", "mail"],
    "data": [
        "security/ir.model.access.csv",
        "views/patient_views.xml",
    ],
    "application": False,
}
