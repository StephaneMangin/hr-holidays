# Copyright 2024 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models

from ..models.hr_employee_hour import TYPE_SELECTION

TYPE_LEAVE_SELECTION = [
    (t_name, t_string) for (t_name, t_string) in TYPE_SELECTION if t_name == "leave"
]


class HrEmployeeHourReport(models.Model):
    _inherit = "hr.employee.hour.report"

    type = fields.Selection(selection_add=TYPE_LEAVE_SELECTION)

    def where_types(self):
        return super().where_types() + ["leave"]
