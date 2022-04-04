{
    "name": "partner",
    "version": "15.0.0.1.0",
    "depends": ["partner_firstname", "crm"],
    "description": """""",
    "data": [
        "security/ir.model.access.csv",
        "views/liabilities_views.xml",
        "views/res_partner_views.xml",
        "views/crm_lead_views.xml",

    ],
    "application": True,
    "installable": True,
    "sequence": -100,
    "license": "LGPL-3",
}