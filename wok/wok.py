import pathlib

from wok.job import Job
from wok.task import Task


class Wok:
    """The Work Kounter main object.
    It has a jobs list and a current_job_idx index.
    It defines default_dir to $HOME/.wok


    """

    default_dir = pathlib.Path.home() / ".wok"

    def __init__(self):
        self.jobs = []
        self.current_job_idx = -1

    def __check_dir(self, dir):
        if dir.exists() and not dir.is_dir():
            print(f"ERROR: {dir} exists and is not a dir!")
            return False
        if not dir.exists():
            dir.mkdir()
        return True

    def __get_current_job(self):
        return None if self.current_job_idx == -1 else self.jobs[self.current_job_idx]

    def status(self):
        """Get the status

        :return: current job, running task(s)
        :rtype: string, [string]

        """
        j, t = "No current job", []
        job = self.__get_current_job()
        if job is not None:
            j = job.__str__()
            tasks = job.get_running_tasks()
            if len(tasks) == 0:
                t.append("No running task")
            else:
                for task in tasks:
                    t.append(task.__str__())
        return j, t

    def suspend(self):
        """Suspend the all running tasks if any

        :return: False if no task to suspend
        :rtype: boolean

        """
        r = False
        for job in self.jobs:
            for task in job.get_running_tasks():
                task.end()
                r = True
        return r

    def switch(self, job_name, create=False):
        """Switch to the job with the given name

        :param job_name: The name of the job to switch to
        :param create: Create the job if it does not exist (Default value = False)
        :return: True if the job was found and selected
        :rtype: boolean

        """
        try:
            job, self.current_job_idx = next(
                ((j, i) for i, j in enumerate(self.jobs) if j.name == job_name)
            )
            return True

        except StopIteration:
            if create:
                job = Job(job_name)
                self.jobs.append(job)
                return self.switch(job_name)
            else:
                return False

    def load(self, dir=default_dir):
        """Load the WoK from the dir folder

        :param dir: Default value = default_dir)

        """
        if not self.__check_dir(dir):
            print("Could not load (see previous error)")
            return False
        # Now dir exists and is a directory
        current_job_name = None
        try:
            current_job_file = [
                x for x in dir.iterdir() if not x.is_dir() and x.name == "current_job"
            ][0]
            current_job_name = current_job_file.read_text().strip()
        except IndexError:
            print("No current job file found")
        for job_file in [x for x in dir.iterdir() if x.is_dir()]:
            job = Job(job_file.name)
            for task_file in job_file.iterdir():
                task = Task(task_file.name)
                task.load(task_file.read_text())
                job.add_task(task)
            self.jobs.append(job)
            if job.name == current_job_name:
                self.current_job_idx = len(self.jobs) - 1

    def save(self, dir=default_dir):
        """Save the WoK to the dir folder

        :param dir: Default value = default_dir)

        """
        if not self.__check_dir(dir):
            print("Could not save (see previous error)")
            return False
        for i, job in enumerate(self.jobs):
            if i == self.current_job_idx:
                (dir / "current_job").write_text(job.name)
            job_dir = dir / job.name
            try:
                job_dir.mkdir()
            except FileExistsError:
                [f.unlink() for f in job_dir.iterdir()]
            for task in job.tasks:
                (job_dir / task.name).write_text(task.save())
