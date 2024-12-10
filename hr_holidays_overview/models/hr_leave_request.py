# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class HolidaysRequest(models.Model):
    _name = "hr.leave"
    _inherit = ["hr.leave", "hr.employee.hour.mixin"]

    def prepare_hr_employee_hour_values(self, **kwargs):
        model_id = self._get_model_id()
        values_list = []
        for leave in self:
            days_qty = leave.number_of_days
            hours_qty = leave.number_of_hours_display
            leave_type = leave.holiday_status_id
            project = leave_type.timesheet_project_id
            task = leave_type.timesheet_task_id
            values = {
                "model_id": model_id,
                "res_id": leave.id,
                "name_id": f"{leave_type._name},{leave_type.id}",
                "type": "leave_request",
                "date": leave.date_from,
                "active": leave_type.active,
                "hours_qty": hours_qty,
                "days_qty": days_qty,
                "state": leave.state,
                "unplanned": leave_type.requires_allocation == "no",
                "project_id": project.id,
                "task_id": task.id,
            }
            # Needed for a manager to request for multiple employees
            for employee in leave.employee_ids or leave.employee_id:
                values_list.append({"employee_id": employee.id, **values})
        return values_list
