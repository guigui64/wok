import shutil
from pathlib import Path
from typing import List, Tuple

from tabulate import tabulate
from wok.job import Job
from wok.task import Task


class Wok:
    """The Work Kounter main object.
    It has a jobs list and a current_job_idx index.
    It defines default_dir to $HOME/.wok


    """

    default_dir: Path = Path.home() / ".wok"

    def __init__(self):
        self.jobs: List[Job] = []
        self.current_job_idx: int = -1

    @staticmethod
    def check_dir(dir: Path) -> bool:
        if dir.exists() and not dir.is_dir():
            print(f"ERROR: {dir} exists and is not a dir!")
            return False
        if not dir.exists():
            dir.mkdir()
        return True

    def load(self, dir: Path = default_dir) -> Tuple[bool, str]:
        """Load the WoK from the dir folder

        :param dir: Default value = default_dir
        :return: True if success + message
        :rtype: boolean, string

        """
        if not Wok.check_dir(dir):
            return False, "Could not load (see previous error)"
        # Now dir exists and is a directory
        current_job_name = None
        try:
            current_job_file = [
                x for x in dir.iterdir() if not x.is_dir() and x.name == "current_job"
            ][0]
            current_job_name = current_job_file.read_text().strip()
        except IndexError:
            pass
        for job_file in [x for x in dir.iterdir() if x.is_dir()]:
            job = Job(job_file.name)
            for task_file in job_file.iterdir():
                task = Task(task_file.name)
                task.load(task_file.read_text().split("\n"))
                job.add_task(task)
            self.jobs.append(job)
            if job.name == current_job_name:
                self.current_job_idx = len(self.jobs) - 1
        return True, "Loaded successfully"

    def save(self, dir=default_dir) -> Tuple[bool, str]:
        """Save the WoK to the dir folder

        :param dir: Default value = default_dir)
        :return: True if success + message
        :rtype: boolean, string

        """
        if dir.exists():
            shutil.rmtree(dir)
        if not Wok.check_dir(dir):
            return False, "Could not load (see previous error)"
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
        return True, "Loaded successfully"

    def detailed_table(self) -> str:
        out = tabulate([["***** Wok details *****"]], tablefmt="fancy_grid")
        out += "\n"
        if self.current_job_idx != -1:
            out += self.jobs[self.current_job_idx].detailed_table(
                title="current job",
                suffix=[
                    [
                        "detailed tasks",
                        "\n".join(
                            [
                                task.detailed_table(time=False)
                                for task in self.jobs[self.current_job_idx].tasks
                            ]
                        ),
                    ]
                ],
            )
            out += "\n"
        for i, job in enumerate(self.jobs):
            if i != self.current_job_idx:
                out += job.detailed_table(
                    suffix=[
                        [
                            "detailed tasks",
                            "\n".join(
                                [task.detailed_table(time=False) for task in job.tasks]
                            ),
                        ]
                    ],
                )
                out += "\n"
        return out
