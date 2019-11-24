WoK - the Work Kounter
======================

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
| pause   | Pause the current task                        |
+---------+-----------------------------------------------+
| resume  | Resume the current task                       |
+---------+-----------------------------------------------+
| job     | Handle jobs (list, add, delete)               |
+---------+-----------------------------------------------+
| task    | Handle tasks (list, add, delete, start, stop) |
+---------+-----------------------------------------------+
| stat    | | Display statistics                          |
|         | | ``wok [options] stat <job> [<task>]``       |
+---------+-----------------------------------------------+

Model
-----

+------+------------------------------------------------------+----------------------------------------------------------------------------+
| Term | Definition                                           | Example commands                                                           |
+======+======================================================+============================================================================+
| Job  | A job                                                | | ``wok job`` or ``wok job --list`` to list existing jobs                  |
|      |                                                      | | ``wok job my_job`` to add the *my_job* job                               |
|      |                                                      | | ``wok job --delete my_job`` to remove this job                           |
|      |                                                      | | ``wok switch my_job`` to switch to this job                              |
+------+------------------------------------------------------+----------------------------------------------------------------------------+
| Task | A task from a job (a task cannot be shared between   | | ``wok task`` or ``wok task --list`` to list all tasks of the current job |
|      | jobs, create a *generic* job if you have such tasks) | | ``wok task my_task`` to add the *my_task* task                           |
|      |                                                      | | ``wok task my_task start`` to register you started working on this task  |
|      |                                                      | | ``wok pause`` will pause any started task                                |
+------+------------------------------------------------------+----------------------------------------------------------------------------+
|      |                                                      |                                                                            |
+------+------------------------------------------------------+----------------------------------------------------------------------------+

Installing
----------

*TBD* pip ?

Contributing
------------

Clone this repo and use `pipenv install --dev` to install all needed
dependencies then start coding.

