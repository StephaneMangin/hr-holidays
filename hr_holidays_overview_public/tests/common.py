# Copyright 2022 Camptocamp SA
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl)

from datetime import datetime

from odoo.addons.hr_timesheet_overview.tests.common import HrDashboardCommon


class HrDashboardHolidaysPublicCommon(HrDashboardCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.public_holiday = cls.env["hr.holidays.public"].create(
            {"year": 2022, "country_id": cls.employee.country_id.id}
        )
        cls.public_holiday_line = cls.env["hr.holidays.public.line"].create(
            {
                "name": "Public Holiday Sample",
                "date": datetime(2022, 1, 10),
                "year_id": cls.public_holiday.id,
            }
        )
