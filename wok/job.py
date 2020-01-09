from datetime import timedelta
from typing import List, Optional, Tuple

from tabulate import tabulate
from wok.task import Task


class Job:
    """A Job has a name and a list of tasks."""

    def __init__(self, name: str):
        self.name: str = name
        self.tasks: List[Task] = []

    def add_task(self, task: Task) -> Tuple[bool, str]:
        """Adds the task if the name is not taken

        :param task: The task to add
        :type task: Task
        :return: True for success + message
        :rtype: boolean, string

        """
        if self.get_task(task.name):
            return (
                False,
                f"A task with name '{task.name}' already exists in job '{self.name}'",
            )
        self.tasks.append(task)
        return True, f"Task '{task.name}' added to job '{self.name}'"

    def remove_task(self, task: Task) -> Tuple[bool, str]:
        """

        :param task: The task to remove
        :type task: Task
        :return: True for success + message
        :rtype: boolean, string

        """
        try:
            self.tasks.remove(task)
            return True, f"Task '{task.name}' removed from job '{self.name}'"
        except ValueError:
            return False, "No task to remove"

    def get_task(self, taskname: str) -> Optional[Task]:
        """

        :param taskname: The name of the task to get
        :type taskname: string
        :return: the task or None if not found
        :rtype: Task

        """
        try:
            return next(filter(lambda t: t.name == taskname, self.tasks))
        except StopIteration:
            return None

    def get_running_tasks(self) -> List[Task]:
        """

        :return: the running tasks
        :rtype: [Task]

        """
        return [t for t in self.tasks if t.is_running()]

    def remove_task_name(self, taskname: str) -> Tuple[bool, str]:
        """

        :param taskname: The name of the task to remove
        :type taskname: string
        :return: True for success + message
        :rtype: boolean, string

        """
        return self.remove_task(self.get_task(taskname))

    def __str__(self):
        s = f"Job '{self.name}'\n"
        for task in self.tasks:
            if task.is_running():
                s += f"\t{task} [running]\n"
            else:
                s += f"\t{task}\n"
        return s[:-1]  # Remove last \n

    def detailed_table(self, title: str = "Job", suffix: List[str] = []) -> str:
        tasks = [(t, t.get_total_duration()) for t in self.tasks]
        total = sum([d for (t, d) in tasks], timedelta(0))
        tasks_data = [
            [
                t.name,
                "yes" if t.is_running() else "no",
                Task.duration_to_str(d),
                "N/A" if total == 0 else f"{d / total:.2%}",
            ]
            for (t, d) in tasks
        ]
        tasks_table = tabulate(
            tasks_data, ["name", "running", "duration", "ratio"], tablefmt="fancy_grid"
        )
        return tabulate(
            [["tasks", tasks_table], ["total duration", Task.duration_to_str(total)]]
            + suffix,
            [title, self.name],
            tablefmt="fancy_grid",
        )
