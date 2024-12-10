# Copyright 2022 Camptocamp SA
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl)
from datetime import datetime

from freezegun import freeze_time

from odoo.addons.hr_timesheet_overview.tests.common import HrDashboardCommon


@freeze_time("2021-01-01")
class HrDashboardHolidaysCommon(HrDashboardCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.paid_type = cls.env.ref("hr_holidays.holiday_status_cl")
        cls.unpaid_type = cls.env.ref("hr_holidays.holiday_status_sl")
        cls.paid_type.write(
            {"timesheet_project_id": cls.project.id, "timesheet_task_id": cls.task.id}
        )
        number_of_days = 30
        cls.leave_allocation_previous_year = cls.env["hr.leave.allocation"].create(
            {
                "employee_id": cls.employee.id,
                "name": "Allocation for the whole year",
                "allocation_type": "accrual",
                "state": "confirm",
                "holiday_status_id": cls.paid_type.id,
                "date_from": datetime(2021, 1, 1).date(),
                "number_of_days": number_of_days,
                "holiday_type": "employee",
            }
        )
        # cls.leave_allocation_previous_year._compute_number_of_days_display()
        cls.leave_allocation_previous_year._compute_from_holiday_status_id()
        cls.leave_allocation_previous_year.action_validate()
        cls.leave_allocation_current_year = cls.env["hr.leave.allocation"].create(
            {
                "employee_id": cls.employee.id,
                "name": "Allocation for the whole year",
                "allocation_type": "regular",
                "state": "confirm",
                "holiday_status_id": cls.paid_type.id,
                "date_from": datetime(2022, 1, 1).date(),
                "number_of_days": number_of_days,
                "holiday_type": "employee",
            }
        )
        # cls.leave_allocation_current_year._compute_number_of_days_display()
        cls.leave_allocation_current_year._compute_from_holiday_status_id()
        cls.leave_allocation_current_year.action_validate()
        cls.leave_request = cls.env["hr.leave"].create(
            {
                "employee_id": cls.employee.id,
                "name": "Request for christmas",
                "state": "confirm",
                "holiday_status_id": cls.paid_type.id,
                "request_date_from": datetime(2021, 12, 24).date(),
                "request_date_to": datetime(2022, 1, 6).date(),
                "date_from": datetime(2021, 12, 24).date(),
                "date_to": datetime(2022, 1, 6).date(),
                "holiday_type": "employee",
            }
        )
        cls.leave_request._compute_number_of_days()
        cls.leave_request._compute_date_from_to()
        cls.leave_request.action_validate()
