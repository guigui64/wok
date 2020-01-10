from pathlib import Path
from typing import Optional, Tuple

from wok.job import Job
from wok.task import Task
from wok.wok import Wok

ApiRtype = Tuple[bool, str]


class WokApi:
    def __init__(self, dir: Path = Wok.default_dir):
        self.wok: Wok = Wok()
        self.dir = dir

    def load(self) -> ApiRtype:
        return self.wok.load(self.dir)

    def save(self) -> ApiRtype:
        self.wok.save(self.dir)

    def get_current_job(self) -> Optional[Job]:
        return (
            None
            if self.wok.current_job_idx == -1
            else self.wok.jobs[self.wok.current_job_idx]
        )

    @staticmethod
    def __validate_name(name: str) -> bool:
        return not (
            any([char in name for char in r".-+/\:*?|<>"]) or "current_job" in name
        )

    def add_job(self, name: str, current: bool = False) -> ApiRtype:
        if not WokApi.__validate_name(name):
            return False, "Job name cannot contain a '.'"
        if any([job.name == name for job in self.wok.jobs]):
            return False, f"Job with name '{name}' already exists"
        job = Job(name)
        self.wok.jobs.append(job)
        if current:
            self.wok.current_job_idx = len(self.wok.jobs) - 1
        return True, f"Job '{name}' created"

    def add_task(self, name: str) -> ApiRtype:
        if not WokApi.__validate_name(name):
            return False, "Task name cannot contain a '.'"
        job = self.get_current_job()
        if job is None:
            return False, "No current job to add a task to"
        if any([task.name == name for task in job.tasks]):
            return False, f"Task with name '{name}' already exists in job '{job.name}'"
        task = Task(name)
        job.add_task(task)
        return True, f"Task '{name}' created"

    def list_jobs(self) -> ApiRtype:
        out = ""
        for i, j in enumerate(self.wok.jobs):
            if i == self.wok.current_job_idx:
                out += j.name + " [current]\n"
            else:
                out += j.name + "\n"
        if len(out) == 0:
            return False, "No job"
        return True, out[:-1]  # remove last \n

    def list_current_job_tasks(self) -> ApiRtype:
        job = self.get_current_job()
        out = ""
        if job is not None:
            for task in job.tasks:
                if task.is_running():
                    out += task.name + " [running]\n"
                else:
                    out += task.name + "\n"
        if len(out) == 0:
            return False, "No task"
        return True, out[:-1]

    def __get_job(self, name: str) -> Optional[Job]:
        return next(filter(lambda job: job.name == name, self.wok.jobs), None)

    def __get_task(self, name: str) -> Optional[Task]:
        job = self.get_current_job()
        if job is None:
            return None
        return next(filter(lambda task: task.name == name, job.tasks), None)

    def delete_job(self, name: str) -> ApiRtype:
        current = self.get_current_job()
        job = self.__get_job(name)
        if job is None:
            return False, f"No job '{name}' found to delete"
        self.wok.jobs.remove(job)
        if current.name == name:
            self.wok.current_job_idx = -1
        else:
            _, self.wok.current_job_idx = next(
                ((j, i) for i, j in enumerate(self.wok.jobs) if j.name == current.name)
            )
        return True, f"Job '{name}' deleted!"

    def delete_task(self, name: str) -> ApiRtype:
        job = self.get_current_job()
        task = self.__get_task(name)
        if task is None:
            if job is None:
                return False, "No current job"
            return False, f"No task '{name}' found in current job '{job.name}'"
        job.tasks.remove(task)
        return True, f"Task '{name}' deleted from current job '{job.name}'"

    def rename_job(self, old_name: str, new_name: str) -> ApiRtype:
        job = self.__get_job(old_name)
        if job is None:
            return False, f"Could not find job '{old_name}'"
        if self.__get_job(new_name) is not None:
            return (
                False,
                f"A job with name '{new_name}' already exists",
            )
        job.name = new_name
        return True, f"Job '{old_name}' renamed '{new_name}' successfully"

    def rename_task(self, old_name: str, new_name: str) -> ApiRtype:
        job = self.get_current_job()
        if job is None:
            return False, "No current job"
        if self.__get_task(new_name) is not None:
            return False, f"A task with name '{new_name}' already exists"
        task = self.__get_task(old_name)
        if task is None:
            return (
                False,
                f"No task named '{old_name}' to rename in current job '{job.name}'",
            )
        task.name = new_name
        return True, f"Task '{old_name}' renamed '{new_name}' successfully"

    def get_job_details(self, name: str, table: bool = False) -> ApiRtype:
        job = self.__get_job(name)
        if job is None:
            return False, f"No job '{name}' found"
        if table:
            return True, job.detailed_table()
        return True, str(job)

    def get_task_details(self, name: str, table: bool = False) -> ApiRtype:
        job = self.get_current_job()
        task = self.__get_task(name)
        if task is None:
            if job is None:
                return False, "No current job"
            return False, f"No task '{name}' found in current job '{job.name}'"
        if table:
            return True, task.detailed_table()
        return True, task.detailed_str()

    def __handle_path(self, path: str) -> Tuple[bool, str, str, str]:
        if "." in path:
            job_name, task_name = path.split(".")
            job = self.__get_job(job_name)
            if job is None:
                return (
                    False,
                    f"No job with name '{job_name}' found",
                    job_name,
                    task_name,
                )
            if job != self.get_current_job():
                switched, msg = self.switch(job_name)
                return switched, msg, job_name, task_name
            return True, "", job_name, task_name
        else:
            job = self.get_current_job()
            if job is None:
                return False, "No current job", "", ""
            return True, "", job.name, path

    def start(self, path: str, create: bool = False) -> ApiRtype:
        res, msg, job_name, task_name = self.__handle_path(path)
        if not res:
            return res, msg
        out = "" if msg == "" else msg + "\n"
        task = self.__get_task(task_name)
        if task is None:
            if not create:
                return (
                    False,
                    out
                    + f"No task named '{task_name}' found in current job '{job_name}'",
                )
            added, msg = self.add_task(task_name)
            if not added:
                return False, msg
            out += msg + "\n"
            task = self.__get_task(task_name)
        started, msg = task.start()
        return started, out + msg

    def end(self, path: str, create: bool = False) -> ApiRtype:
        res, msg, job_name, task_name = self.__handle_path(path)
        if not res:
            return res, msg
        out = "" if msg == "" else msg + "\n"
        task = self.__get_task(task_name)
        if task is None:
            return (
                False,
                out + f"No task '{task_name}' found in current job '{job_name}'",
            )
        ended, msg = task.end()
        return ended, out + msg

    def status(self) -> ApiRtype:
        j, t = "No current job", []
        job = self.get_current_job()
        if job is not None:
            j = f"Job '{job.name}'"
            tasks = job.get_running_tasks()
            if len(tasks) == 0:
                t.append("No running task")
            else:
                for task in tasks:
                    t.append(task.__str__())
        else:
            t.append("No running task")
        out = "Current job:\n"
        out += "\t" + j + "\n\n"
        out += "Running task(s):\n"
        out += "\n".join(["\t" + tt for tt in t])
        return True, out

    def suspend(self) -> ApiRtype:
        r = []
        for job in self.wok.jobs:
            for task in job.get_running_tasks():
                r.append(task.end())
        if len(r) == 0:
            return False, "No task to suspend"
        return any([b for b, _ in r]), "\n".join([m for _, m in r])

    def switch(self, job_name: str, create: bool = False) -> ApiRtype:
        if (
            self.get_current_job() is not None
            and self.get_current_job().name == job_name
        ):
            return False, f"Already on job '{job_name}'"
        # suspend all running tasks before switching
        suspended, suspend_out = self.suspend()
        if suspended:
            suspend_out = suspend_out + "\n"
        else:
            suspend_out = ""
        ok = True, suspend_out + f"Switched to job '{job_name}'"
        ko = (
            False,
            suspend_out
            + f"Impossible to switch to job '{job_name}', try using the '-c' option",
        )
        try:
            _, self.wok.current_job_idx = next(
                ((j, i) for i, j in enumerate(self.wok.jobs) if j.name == job_name)
            )
            return ok

        except StopIteration:
            if create:
                self.add_job(job_name, current=True)
                return ok
            else:
                return ko

    def get_details(self) -> ApiRtype:
        return True, self.wok.detailed_table()
