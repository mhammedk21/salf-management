{
    "name": "Financial Loans Management",
    "version": "19.0.1.0.0",
    "category": "Accounting",
    "summary": "Customer records and one-time financial loan tracking",
    "description": "Free community add-on for managing customers, one loan per customer, disbursement and full repayment receipts.",
    "author": "Custom Community Module",
    "license": "LGPL-3",
    "depends": ["base", "web"],
    "data": [
        "security/loan_security.xml",
        "security/ir.model.access.csv",
        "views/customer_views.xml",
        "views/loan_views.xml",
        "views/dashboard_views.xml",
        "reports/loan_receipts.xml",
        "views/menu.xml"
    ],
    "installable": True,
    "application": True
}
