# Copyright 2022 Camptocamp SA
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl)

from .common import HrDashboardHolidaysPublicCommon


class HrEmployeeHourTests(HrDashboardHolidaysPublicCommon):
    def test_prepare_attendance_value_for_public_holiday_dates(self):
        public_holiday = self.public_holiday_line.date
        values = self.current_contract.prepare_hr_employee_hour_values()
        self.assertTrue(
            all([value["date"] != public_holiday for value in values]),
            f"This public holiday date {public_holiday} should not generate "
            f"an employee hour for this contract {self.current_contract.name}",
        )
