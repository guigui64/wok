from datetime import datetime, timedelta
from typing import List, Tuple


class Task:
    """A Task has a name and datetimes when the user worked on it."""

    isoformat: str = "%Y-%m-%dT%H:%M:%S.%f"
    niceformat: str = "%H:%M:%S (%Y-%m-%d)"

    def __init__(self, name: str):
        self.name: str = name
        self.datetimes: List[Tuple[datetime, datetime]] = []
        self.current_datetime: datetime = None

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
        self.current_datetime = None
        sduration = str(duration)
        try:
            sduration = sduration[: sduration.rindex(".")]  # remove milliseconds
        except ValueError:
            pass  # not found
        return (
            True,
            f"{self} ended at {dt.strftime(Task.niceformat)}\n\tDuration={duration}",
        )

    def load(self, input: List[str]) -> None:
        """Loads a task from the content of its file.

        :param input: A list of lines
        :type input: [string]

        """
        if self.current_datetime:
            print(f"ERR: {self} current datetime will be lost: {self.current_datetime}")
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

    def get_total_duration(self, now: datetime = datetime.now()) -> str:
        duration = sum(
            [dt[1] - dt[0] for dt in self.datetimes],
            timedelta(0)
            if self.current_datetime is None
            else now - self.current_datetime,
        )
        sduration = str(duration)
        try:
            sduration = sduration[: sduration.rindex(".")]  # remove milliseconds
        except ValueError:
            pass  # not found
        return sduration

    def detailed_str(self):
        now = datetime.now()
        out = str(self)
        if len(self.datetimes) > 0:
            if self.is_running():
                out += " [running]"
            out += "\n"
            out += self.datetimes[0][0].strftime(Task.niceformat)
            # TODO format duration
            out += " -[" + str(self.get_total_duration(now)) + "]-> "
            out += (
                self.datetimes[-1][1] if self.current_datetime is None else now
            ).strftime(Task.niceformat)
        return out
