from datetime import datetime, timedelta
from typing import List, Tuple

from tabulate import tabulate


class Task:
    """A Task has a name and datetimes when the user worked on it."""

    isoformat: str = "%Y-%m-%dT%H:%M:%S.%f"
    niceformat: str = "%H:%M:%S (%Y-%m-%d)"

    def __init__(self, name: str):
        self.name: str = name
        self.datetimes: List[Tuple[datetime, datetime]] = []
        self.current_datetime: datetime = None

    @staticmethod
    def duration_to_str(duration: timedelta) -> str:
        sec = duration.total_seconds()
        hours = sec // 3600
        sec = sec - hours * 3600
        minutes = sec // 60
        sec = sec - minutes * 60
        return f"{int(hours):02}:{int(minutes):02}:{int(sec):02}"

    def start(self, dt: datetime = datetime.now()) -> Tuple[bool, str]:
        """

        :param dt:  (Default value = datetime.now())
        :return: True for success + message
        :rtype: boolean, string

        """
        if self.current_datetime:
            return False, f"{self} already started"
        self.current_datetime = dt
        return (
            True,
            f"{self} started at {self.current_datetime.strftime(Task.niceformat)}",
        )

    def is_running(self) -> bool:
        """

        :return: True if task is running
        :rtype: boolean

        """
        return self.current_datetime is not None

    def end(self, dt: datetime = datetime.now()) -> Tuple[bool, str]:
        """

        :param dt:  (Default value = datetime.now())
        :return: True for success + message
        :rtype: boolean, string

        """
        if not self.is_running():
            return False, f"{self} not yet started"
        duration = dt - self.current_datetime
        self.datetimes.append((self.current_datetime, dt))
        last_started = self.current_datetime
        self.current_datetime = None
        sduration = Task.duration_to_str(duration)
        return (
            True,
            f"{self} ended at {dt.strftime(Task.niceformat)}"
            + f"\n\tDuration={sduration} ({last_started.strftime(Task.niceformat)})",
        )

    def load(self, input: List[str]) -> None:
        """Loads a task from the content of its file.

        :param input: A list of lines
        :type input: [string]

        """
        if self.current_datetime:
            print(
                f"ERROR: {self} current datetime will be lost: {self.current_datetime}"
            )
            self.current_datetime = None
        self.datetimes.clear()
        for line in input:
            if "->" in line:
                self.datetimes.append(
                    tuple(
                        datetime.strptime(x, Task.isoformat) for x in line.split("->")
                    )
                )
            elif line.startswith("C:"):
                self.current_datetime = datetime.strptime(line[2:], Task.isoformat)

    def save(self) -> str:
        """Saves the task to a string to be written to its file.

        :return: The content of the file to be written
        :rtype: string

        """
        output = "\n".join(
            [
                "->".join([d.strftime(Task.isoformat) for d in dt])
                for dt in self.datetimes
            ]
        )
        if self.current_datetime:
            if len(output) > 0:
                output += "\n"
            output += "C:" + self.current_datetime.strftime(Task.isoformat)
        return output

    def __str__(self):
        return f"Task '{self.name}'"

    def get_total_duration(self, now: datetime = datetime.now()) -> timedelta:
        duration = sum(
            [dt[1] - dt[0] for dt in self.datetimes],
            timedelta(0)
            if self.current_datetime is None
            else now - self.current_datetime,
        )
        return duration

    def get_current_duration(self, now: datetime = datetime.now()) -> timedelta:
        if self.current_datetime is None:
            return timedelta(0)
        return now - self.current_datetime

    def detailed_str(self) -> Tuple[str]:
        now = datetime.now()
        out = (str(self),)
        if self.is_running():
            out += (
                f"started at {self.current_datetime.strftime(Task.niceformat)} "
                + f"running for {Task.duration_to_str(self.get_current_duration(now))}",
            )
        return out

    def detailed_table(self, suffix: List[str] = [], time: bool = True) -> str:
        now = datetime.now()
        time_data = [
            [fro_m.strftime(Task.niceformat), to.strftime(Task.niceformat)]
            for (fro_m, to) in self.datetimes
        ]
        time_table = tabulate(time_data, ["from", "to"], tablefmt="fancy_grid")
        table = [["running", "yes" if self.is_running() else "no"]]
        if time:
            table += [["time", time_table]]
        if self.is_running():
            table += [["started", self.current_datetime.strftime(Task.niceformat)]]
            table += [
                ["running time", Task.duration_to_str(self.get_current_duration(now))]
            ]
        table += [
            ["total duration", Task.duration_to_str(self.get_total_duration(now))]
        ]
        table += suffix
        return tabulate(table, ["task", self.name], tablefmt="fancy_grid",)
