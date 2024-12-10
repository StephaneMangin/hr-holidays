# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    def prepare_hr_employee_hour_values(self, **kwargs):
        values_list = super().prepare_hr_employee_hour_values(**kwargs)
        leave_timesheets = self.filtered("holiday_id")
        name_ids = {ts.id: ts.account_id.id for ts in leave_timesheets}
        for values in values_list:
            if values["res_id"] in name_ids:
                account_id = name_ids[values["res_id"]]
                values["type"] = "leave"
                values["name_id"] = f"account.analytic.account,{account_id}"

        return values_list
