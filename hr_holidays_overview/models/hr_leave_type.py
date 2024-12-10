# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class HrLeaveType(models.Model):
    _inherit = "hr.leave.type"

    def write(self, vals):
        result = super().write(vals)
        if "active" in vals:
            heh_model = self.env["hr.employee.hour"]
            heh_model.toggle_active_for_records(self, apply_to_name_id=True)
        return result
