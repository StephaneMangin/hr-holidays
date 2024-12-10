This module removes public holidays from attendances.

Technical Details
=================

    * On ``hr.contract`` model:
        * Override ``prepare_hr_employee_hour_values`` to remove public holidays from the result.
