# -*- coding: utf-8 -*-
{
    "name": "HIS Core",
    "summary": "Core data model for Hospital Information System",
    "version": "16.0.1.0.0",
    "author": "You",
    "license": "LGPL-3",
    "category": "Healthcare",
    "depends": ["base", "mail"],
    "data": [
        "security/ir_model_access.csv",
        "data/sequence.xml",
        "views/menu.xml",
        "views/patient_views.xml",
        "views/encounter_views.xml",
    ],
    "application": True,
}
