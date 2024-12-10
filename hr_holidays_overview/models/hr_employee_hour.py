# Copyright 2024 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import _, fields, models

TYPE_SELECTION = [
    ("leave", _("Leave")),
    ("leave_request", _("Leave Request")),
    ("leave_allocation", _("Leave Allocation")),
]
ONDELETE_SELECTION = {
    "leave": "set default",
    "leave_request": "set default",
    "leave_allocation": "set default",
}


class HrEmployeeHour(models.Model):
    _inherit = "hr.employee.hour"

    type = fields.Selection(
        selection_add=TYPE_SELECTION,
        ondelete=ONDELETE_SELECTION,
    )
    state = fields.Selection(
        [
            ("draft", "To Submit"),
            ("cancel", "Cancelled"),
            ("confirm", "To Approve"),
            ("refuse", "Refused"),
            ("validate1", "Second Approval"),
            ("validate", "Approved"),
        ],
    )
    unplanned = fields.Boolean(default=False)
