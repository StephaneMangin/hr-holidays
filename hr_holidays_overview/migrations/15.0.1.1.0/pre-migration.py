# Copyright 2023 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade

from odoo.tools import parse_version


@openupgrade.migrate()
def migrate(env, version):
    if parse_version(version) == parse_version("15.0.1.0.0"):
        openupgrade.logged_query(
            env.cr, """DROP VIEW IF EXISTS hr_employee_leave_report;"""
        )
        openupgrade.logged_query(
            env.cr,
            """
UPDATE hr_employee_hour
SET name_id = CONCAT('hr.leave.type', ',', hlt.leave_type_id)
FROM (
    SELECT hla.id AS allocation_id, hlt.id AS leave_type_id
    FROM hr_leave_type AS hlt
    JOIN hr_leave_allocation AS hla ON hla.holiday_status_id = hlt.id
) AS hlt
WHERE hlt.allocation_id = res_id AND type = 'leave_allocation';""",
        )
        openupgrade.logged_query(
            env.cr,
            """
UPDATE hr_employee_hour
SET name_id = CONCAT('hr.leave.type', ',', hlt.leave_type_id)
FROM (
    SELECT hl.id AS request_id, hlt.id AS leave_type_id
    FROM hr_leave_type AS hlt
    JOIN hr_leave AS hl ON hl.holiday_status_id = hlt.id
) AS hlt
WHERE hlt.request_id = res_id AND type = 'leave_request';""",
        )
