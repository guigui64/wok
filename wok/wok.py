import pathlib

from wok.job import Job
from wok.task import Task


class Wok:

    default_dir = pathlib.Path.home() / ".wok"

    def __init__(self):
        self.jobs = []
        self.current_job = -1

    def __check_dir(self, dir):
        if dir.exists() and not dir.is_dir():
            print(f"ERROR: {dir} exists and is not a dir!")
            return False
        if not dir.exists():
            dir.mkdir()
        return True

    def load(self, dir=default_dir):
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
                self.current_job = len(self.jobs) - 1

    def save(self, dir=default_dir):
        if not self.__check_dir(dir):
            print("Could not save (see previous error)")
            return False
        for i, job in enumerate(self.jobs):
            if i == self.current_job:
                (dir / "current_job").write_text(job.name)
            job_dir = dir / job.name
            try:
                job_dir.mkdir()
            except FileExistsError:
                [f.unlink() for f in job_dir.iterdir()]
            for task in job.tasks:
                (job_dir / task.name).write_text(task.save())
