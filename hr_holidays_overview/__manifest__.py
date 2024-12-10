# Copyright 2024 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "HR Holidays Overview",
    "version": "15.0.1.3.0",
    "license": "AGPL-3",
    "category": "Human Resources",
    "website": "https://github.com/OCA/hr-holidays",
    "author": "Camptocamp SA, Odoo Community Association (OCA)",
    "depends": ["hr_timesheet_overview", "project_timesheet_holidays"],
    "data": [
        "security/ir.model.access.csv",
        "views/hr_employee_hour_views.xml",
        "wizards/hr_employee_hour_updater_view.xml",
        "report/hr_employee_leave_report_views.xml",
    ],
    "installable": True,
}
