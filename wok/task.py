from datetime import datetime


class Task:
    """A Task has a name and datetimes when the user worked on it."""

    isoformat = "%Y-%m-%dT%H:%M:%S.%f"

    def __init__(self, name):
        self.name = name
        self.datetimes = []
        self.current_datetime = None

    def start(self, dt=datetime.now()):
        """

        :param dt:  (Default value = datetime.now())
        :return: True for success
        :rtype: boolean

        """
        if self.current_datetime:
            print(f"{self} already started")
            return False
        self.current_datetime = dt
        print(f"{self} started at {self.current_datetime}")
        return True

    def end(self, dt=datetime.now()):
        """

        :param dt:  (Default value = datetime.now())
        :return: True for success
        :rtype: boolean

        """
        if self.current_datetime is None:
            print(f"{self} not yet started")
            return False
        print(f"{self} ended at {dt}")
        duration = dt - self.current_datetime
        print(
            f"\tDuration={duration}"
        )  # TODO format duration (type=timedelta) (use divmod)
        self.datetimes.append([self.current_datetime, dt])
        self.current_datetime = None
        return True

    def load(self, input):
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
                    [datetime.strptime(x, Task.isoformat) for x in line.split("->")]
                )
            elif line.startswith("C:"):
                self.current_datetime = datetime.strptime(line[2:], Task.isoformat)

    def save(self):
        """Saves the task to a list of lines to be written to its file.

        :return: The content of the file to be written
        :rtype: [string]

        """
        output = "\n".join(
            [
                "->".join([d.strftime(Task.isoformat) for d in dt])
                for dt in self.datetimes
            ]
        )
        if self.current_datetime:
            output += "\nC:" + self.current_datetime.strftime(Task.isoformat)
        return output

    def __str__(self):
        return f"Task '{self.name}'"
