# -*- coding: utf-8 -*-
{
    "name": "KM Hospital",
    "version": "16.0.1.0.0",
    "license": "LGPL-3",
    "category": "Healthcare",
    "summary": "Basic hospital management models",
    "depends": ["base", "mail"],
    "data": [
        "security/ir.model_access.csv",
        "data/sequence.xml",
        "views/menu.xml",
        "views/department_views.xml",
        "views/doctor_views.xml",
        "views/patient_views.xml",
        "views/appointment_views.xml",
        "views/test_views.xml",
        "views/test_result_views.xml",
    ],
    "application": True,
}
