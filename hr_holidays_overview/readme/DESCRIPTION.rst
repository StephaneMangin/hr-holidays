The main purpose of this dashboard is to allow employee and manager to have an overview of their time off according to their allocations.

This dashboard will cover the time off with the purpose to have an overview of the time off allocated versus the time off taken.

Detailed requirements
=====================

Dashboard Leaves report
-----------------------

Should show the allocated time off and the time off request with an aggregation per time off type / employee / date available per hours or days.
The sum of both colum (allocated/request) will represent the time of available for request.

In order that the employee see easily the current situation by default the view should filter data according the following rules:

- Leaves from archived time off type should be hide by default
- By default we see only the planned time off (allocation_type is fixed or fixed_allocation) and the option should be to add the unplanned (allocation_type is no) or see only the unplanned
- The default view should be by leave_type (and not date)

Global requirement
------------------
The data coming from the time off should always represent the situation we get if we go to the time off app (I mean by here that the data should be in real time).

At the initialisation the system should be able to generate the past data.

Security
--------

The employee should not see the data from the others employee.
One exception for a manager that can see all the data from employees he is the manager of.

Pitfalls
========

- Limit cases about hours on weekend and hours worked at night inbetween 2 days.

Technical Details
=================

  * On ``hr.employee.hour`` model:
      * Override ``_compute_name_id`` to update name for non leaves type
      * Add ``unplanned`` boolean field related
      * Add ``state`` selection field
      * Add new selection options for ``type`` field

  * On ``hr.leave.allocation`` model:
      * Override method ``prepare_hr_employee_hour_values`` to update values before create

  * On ``hr.leave.type`` model:
      * Override ``write`` method to archive ``hr.employee.hour`` related to the leave type

  * On ``hr.leave`` model:
      * Override method ``prepare_hr_employee_hour_values`` to update values before create

  * On ``account.analytic.line`` model:
      * Override method ``prepare_hr_employee_hour_values`` to update values before create

  * On ``hr.employee.hour.report`` model:
      * Add new selection options for ``type`` field
      * Update ``WHERE`` query method to use the ``type`` field

  * On ``hr.employee.leave.report`` model:
      * Add ``unplanned`` boolean field related
      * Add ``state`` selection field
      * Add ``dayofweek`` char field
      * Add new selection options for ``type`` field
