# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from datetime import datetime

from .common import HrDashboardHolidaysCommon


class HrLeaveRequestTests(HrDashboardHolidaysCommon):
    def test_create_employee_hours_from_leave_request(self):
        heh_lines = self._get_related_hours(self.leave_request)
        self.assertEqual(1, len(heh_lines))
        self.assertEqual(
            self.leave_request.number_of_days, sum(heh_lines.mapped("days_qty"))
        )
        self.assertEqual(
            self.leave_request.number_of_hours_display,
            round(sum(heh_lines.mapped("hours_qty")), 4),
        )

    def test_update_employee_hours_from_leave_request(self):
        new_number_of_days = 22
        new_number_of_hours = 64.0
        self.leave_request.write({"number_of_days": new_number_of_days})
        heh_lines = self._get_related_hours(self.leave_request)
        self.assertEqual(1, len(heh_lines))
        self.assertEqual(new_number_of_days, sum(heh_lines.mapped("days_qty")))
        self.assertEqual(
            new_number_of_hours, round(sum(heh_lines.mapped("hours_qty")), 4)
        )

    def test_delete_employee_hours_from_leave_request(self):
        self.leave_request.write({"state": "draft"})
        deleted_id = self.leave_request.id
        self.leave_request.unlink()
        heh_lines = self._get_related_hours(self.leave_request, [deleted_id])
        self.assertEqual(0, len(heh_lines))

    def test_prepare_hr_employee_hour_values_should_always_return_a_list(self):
        values = self.env["hr.leave"].prepare_hr_employee_hour_values()
        self.assertEqual([], values)

    def test_unplanned_sick_leaves_should_be_unplanned_hours(self):
        sick_leave_request = self.env["hr.leave"].create(
            {
                "employee_id": self.employee.id,
                "name": "Request for christmas",
                "state": "confirm",
                "holiday_status_id": self.unpaid_type.id,
                "request_date_from": datetime(2023, 1, 1).date(),
                "request_date_to": datetime(2023, 1, 4).date(),
                "date_from": datetime(2023, 1, 1).date(),
                "date_to": datetime(2023, 1, 4).date(),
                "holiday_type": "employee",
            }
        )
        heh_lines = self._get_related_hours(sick_leave_request)
        self.assertTrue(all(heh_lines.mapped("unplanned")))

    def test_planned_paid_leaves_should_be_planned_hours(self):
        heh_lines = self._get_related_hours(self.leave_request)
        self.assertTrue(all([not heh.unplanned for heh in heh_lines]))
