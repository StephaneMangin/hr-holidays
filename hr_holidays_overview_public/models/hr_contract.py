# Copyright 2024 Camptocamp SA
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import models


class HrContract(models.Model):
    _inherit = "hr.contract"

    def prepare_hr_employee_hour_values(self, **kwargs):
        result = super().prepare_hr_employee_hour_values(**kwargs)
        public_model = self.env["hr.holidays.public"]
        return [
            hour
            for hour in result
            if not public_model.is_public_holiday(
                hour["date"], employee_id=hour["employee_id"]
            )
        ]
