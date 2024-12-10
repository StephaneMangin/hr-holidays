# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from .common import HrDashboardHolidaysCommon


class HrEmployeeHourTests(HrDashboardHolidaysCommon):
    def test_prepare_leave_allocation_value(self):
        la_cy = self.leave_allocation_current_year
        ir_model = self.env["ir.model"].search([("model", "=", la_cy._name)])
        oracle = {
            "date": la_cy.date_from,
            "days_qty": la_cy.number_of_days,
            "employee_id": self.employee.id,
            "hours_qty": la_cy.number_of_hours_display,
            "model_id": ir_model.id,
            "res_id": la_cy.id,
            "type": "leave_allocation",
        }
        values = la_cy.prepare_hr_employee_hour_values()
        self.assertEqual(
            len(values),
            1,
        )
        value = values[0]
        self.assertEqual(oracle["date"], value["date"])
        self.assertEqual(oracle["days_qty"], round(value["days_qty"], 4))
        self.assertEqual(oracle["hours_qty"], value["hours_qty"])
        self.assertEqual(oracle["model_id"], value["model_id"])
        self.assertEqual(oracle["res_id"], value["res_id"])
        self.assertEqual(oracle["type"], value["type"])
        self.assertEqual(oracle["employee_id"], value["employee_id"])

    def test_prepare_leave_request_value(self):
        lr = self.leave_request
        ir_model = self.env["ir.model"].search([("model", "=", lr._name)])
        oracle = {
            "date": lr.date_from,
            "days_qty": lr.number_of_days,
            "employee_id": self.employee.id,
            "hours_qty": lr.number_of_hours_display,
            "model_id": ir_model.id,
            "res_id": lr.id,
            "type": "leave_request",
        }
        values = lr.prepare_hr_employee_hour_values()
        self.assertEqual(
            len(values),
            1,
        )
        value = values[0]
        self.assertEqual(oracle["date"], value["date"])
        self.assertEqual(oracle["days_qty"], round(value["days_qty"], 4))
        self.assertEqual(oracle["hours_qty"], value["hours_qty"])
        self.assertEqual(oracle["model_id"], value["model_id"])
        self.assertEqual(oracle["res_id"], value["res_id"])
        self.assertEqual(oracle["type"], value["type"])
        self.assertEqual(oracle["employee_id"], value["employee_id"])

    def test_leave_allocation_name_id(self):
        la_cy = self.leave_allocation_current_year
        oracle = la_cy.holiday_status_id
        heh_line = self.env["hr.employee.hour"].search(
            [("type", "=", "leave_allocation"), ("date", "=", la_cy.date_from)], limit=1
        )
        self.assertEqual(oracle, heh_line.name_id)

    def test_leave_request_name_id(self):
        lr = self.leave_request
        oracle = lr.holiday_status_id
        heh_line = self.env["hr.employee.hour"].search(
            [("type", "=", "leave_request"), ("date", "=", lr.date_from)], limit=1
        )
        self.assertEqual(oracle, heh_line.name_id)

    def test_archive_leave_type(self):
        paid_type = self.env.ref("hr_holidays.holiday_status_cl")
        heh_lines = self.env["hr.employee.hour"].search(
            [("type", "=", "leave_request")]
        )
        paid_type.write({"active": False})
        heh_lines_archived = self.env["hr.employee.hour"].search(
            [("type", "=", "leave_request"), ("active", "=", False)]
        )
        self.assertEqual(heh_lines, heh_lines_archived)

    def test_timesheet_project_id(self):
        ts = self.timesheets[0]
        oracle = self.project
        heh_line = self.env["hr.employee.hour"].search(
            [("type", "=", "timesheet"), ("res_id", "=", ts.id)], limit=1
        )
        self.assertEqual(oracle, heh_line.project_id)

    def test_timesheet_task_id(self):
        ts = self.timesheets[0]
        oracle = self.task
        heh_line = self.env["hr.employee.hour"].search(
            [("type", "=", "timesheet"), ("res_id", "=", ts.id)], limit=1
        )
        self.assertEqual(oracle, heh_line.task_id)
