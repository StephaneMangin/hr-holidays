# Copyright 2024 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models

from ..models.hr_employee_hour import TYPE_SELECTION


class HrEmployeeLeaveReport(models.Model):
    _name = "hr.employee.leave.report"
    _description = "Employee Leave Report"
    _inherit = "hr.employee.hour.report.abstract"
    _auto = False  # Will be processed in init method

    state = fields.Selection(
        [
            ("draft", "To Submit"),
            ("cancel", "Cancelled"),
            ("confirm", "To Approve"),
            ("refuse", "Refused"),
            ("validate1", "Second Approval"),
            ("validate", "Approved"),
        ],
    )
    unplanned = fields.Boolean(default=False)
    dayofweek = fields.Char("Day of Week")
    type = fields.Selection(selection_add=TYPE_SELECTION)

    def select_hook_custom_fields(self):
        return """
            heh.state,
            heh.unplanned,
            to_char(heh.date, 'day') AS dayofweek,
            -- Inject negative value for total calculation
            SUM(CASE
                  WHEN heh.type = 'leave_request' THEN -heh.days_qty
                  ELSE heh.days_qty
            END) AS days_qty,
            SUM(CASE
                  WHEN heh.type = 'leave_request'  THEN -heh.hours_qty
                  ELSE heh.hours_qty
            END) AS hours_qty,
            -- But keep absolute values for specific graph calculation
            SUM(heh.days_qty) AS days_qty_abs,
            SUM(heh.hours_qty) AS hours_qty_abs,
        """

    def where_types(self):
        return ["leave_request", "leave_allocation"]

    def group_by_hook_custom_fields(self):
        return "heh.state, heh.unplanned,"
