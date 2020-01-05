WoK - the Work Kounter
======================

|licence| |black| |flake8| |actions|

.. |licence| image:: https://img.shields.io/badge/License-GPLv3-blue.svg
    :target: https://www.gnu.org/licenses/gpl-3.0

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. |actions| image:: https://github.com/guigui64/wok/workflows/tests/badge.svg
    :target: https://github.com/guigui64/wok/actions

.. |flake8| image:: https://img.shields.io/badge/code%20check-flake8-yellowgreen
    :target: https://pypi.org/project/flake8/

**wok** is a command line work hours counter

Features
--------

* register working time of specific tasks
* display statistics per day, week or month
* etc. (*TBD*)

Usage
-----

+---------+-----------------------------------------------+
| Command | Description                                   |
+=========+===============================================+
| *empty* | Display status (current job, current task)    |
+---------+-----------------------------------------------+
| switch  | Switch to a job                               |
+---------+-----------------------------------------------+
| suspend | Suspend the running tasks if any              |
+---------+-----------------------------------------------+
| job     | Handle jobs (list, add, delete)               |
+---------+-----------------------------------------------+
| task    | Handle tasks (list, add, delete, start, stop) |
+---------+-----------------------------------------------+
| details | Display details of all jobs and tasks         |
+---------+-----------------------------------------------+

Model
-----

+------+------------------------------------------------------+----------------------------------------------------------------------------+
| Term | Definition                                           | Example commands                                                           |
+======+======================================================+============================================================================+
| Job  | A job. A job has a list of tasks.                    | | ``wok job`` or ``wok job --list`` to list existing jobs                  |
|      |                                                      | | ``wok job my_job`` to display *my_job* job details                       |
|      |                                                      | | ``wok job --create my_job`` to create this job                           |
|      |                                                      | | ``wok job --delete my_job`` to remove this job                           |
|      |                                                      | | ``wok switch my_job`` to switch to this job                              |
+------+------------------------------------------------------+----------------------------------------------------------------------------+
| Task | A task from a job (a task cannot be shared between   | | ``wok task`` or ``wok task --list`` to list all tasks of the current job |
|      | jobs, create a *generic* job if you have such tasks) | | ``wok task --create my_task`` to add the *my_task* task                  |
|      |                                                      | | ``wok task --start my_task`` to register you started working on this task|
|      |                                                      | | ``wok suspend`` will suspend any running task                            |
+------+------------------------------------------------------+----------------------------------------------------------------------------+
|      |                                                      |                                                                            |
+------+------------------------------------------------------+----------------------------------------------------------------------------+

Files
-----

Files will be saved in a *.wok* file inside the ``$HOME`` folder.

::

  .wok/
  |-- current_job # contains current job name
  |-- job_one/
  |   |-- task_one # containes task_one datetimes
  |   |-- task_two
  |   |-- ...
  |-- job_two/
  |   |-- task_one
  |   |-- ...
  |-- ...

Installing
----------

*TBD* pip ?

Contributing
------------

Clone this repo and use ``pipenv install --dev`` to install all needed
dependencies then start coding.
