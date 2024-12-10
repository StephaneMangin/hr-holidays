# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from .common import HrDashboardHolidaysCommon


class HrLeaveAllocationTests(HrDashboardHolidaysCommon):
    def test_create_employee_hours_from_leave_allocation(self):
        heh_lines = self._get_related_hours(self.leave_allocation_current_year)
        self.assertEqual(1, len(heh_lines))
        self.assertEqual(
            self.leave_allocation_current_year.number_of_days,
            sum(heh_lines.mapped("days_qty")),
        )
        self.assertEqual(
            self.leave_allocation_current_year.number_of_hours_display,
            round(sum(heh_lines.mapped("hours_qty")), 4),
        )

    def test_update_employee_hours_from_leave_allocation(self):
        new_number_of_days = 22
        new_number_of_hours = 176.0
        self.leave_allocation_current_year.write({"number_of_days": new_number_of_days})
        heh_lines = self._get_related_hours(self.leave_allocation_current_year)
        self.assertEqual(1, len(heh_lines))
        self.assertEqual(new_number_of_days, sum(heh_lines.mapped("days_qty")))
        self.assertEqual(
            new_number_of_hours, round(sum(heh_lines.mapped("hours_qty")), 4)
        )

    def test_delete_employee_hours_from_leave_allocation(self):
        self.leave_allocation_current_year.write({"state": "draft"})
        deleted_id = self.leave_allocation_current_year.id
        self.leave_allocation_current_year.unlink()
        heh_lines = self._get_related_hours(
            self.leave_allocation_current_year, [deleted_id]
        )
        self.assertEqual(0, len(heh_lines))

    def test_prepare_hr_employee_hour_values_should_always_return_a_list(self):
        values = self.env["hr.leave.allocation"].prepare_hr_employee_hour_values()
        self.assertEqual([], values)
