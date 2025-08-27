{
    "name": "HIS Core",
    "summary": "Core Electronic Medical Record (EMR) models: Patient, Encounter, Lab, Prescription",
    "version": "16.0.1.0.0",
    "author": "You",
    "website": "",
    "category": "Healthcare",
    "license": "LGPL-3",
    "depends": ["base", "mail"],
    "data": [
        "security/ir.model.access.csv",
        "views/his_menus.xml",
        "views/patient_views.xml",
        "views/encounter_views.xml",
        "views/lab_views.xml",
        "views/prescription_views.xml",
    ],
    "application": True,
}
