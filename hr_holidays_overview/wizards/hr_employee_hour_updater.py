# Copyright 2023 Camptocamp SA
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
import logging

from odoo import fields, models
from odoo.osv import expression

_logger = logging.getLogger(__name__)


class WizardHrEmployeeHourUpdater(models.TransientModel):
    _inherit = "wizard.hr.employee.hour.updater"

    leave_request_hours = fields.Boolean(default=True)
    leave_allocation_hours = fields.Boolean(default=True)

    def search_allocations_domain(self):
        """Search filter rules for allocations"""
        base_domain = [
            ("employee_id", "in", self.employee_ids.ids),
            ("state", "not in", ("draft", "cancel", "refuse")),
        ]
        date_domain = expression.AND(
            [
                [("write_date", ">=", self.date_from)],
                [("write_date", "<=", self.date_to)],
            ]
        )
        domain = expression.AND([base_domain, date_domain])
        return domain

    def search_requests_domain(self):
        """Search filter rules for requests"""
        base_domain = [
            ("employee_id", "in", self.employee_ids.ids),
            ("state", "not in", ("draft", "cancel", "refuse")),
        ]
        date_domain = expression.AND(
            [
                [("write_date", ">=", self.date_from)],
                [("write_date", "<=", self.date_to)],
            ]
        )
        domain = expression.AND([base_domain, date_domain])
        return domain

    def _prepare_leave_allocation_values(self):
        """Retrieve leave allocations values"""
        hla_model = self.env["hr.leave.allocation"]
        search_domain = self.search_allocations_domain()
        allocations = hla_model.with_context(active_test=False).search(search_domain)
        _logger.info(f"will process {len(allocations)} leave allocation lines")
        return allocations.prepare_hr_employee_hour_values()

    def _prepare_leave_request_values(self):
        """Retrieve leave requests values"""
        hl_model = self.env["hr.leave"]
        search_domain = self.search_requests_domain()
        requests = hl_model.with_context(active_test=False).search(search_domain)
        _logger.info(f"will process {len(requests)} leave request lines")
        return requests.prepare_hr_employee_hour_values()

    def prepare_values(self):
        values = super().prepare_values()
        if self.leave_allocation_hours:
            values.extend(self._prepare_leave_allocation_values())
        if self.leave_request_hours:
            values.extend(self._prepare_leave_request_values())
        return values
