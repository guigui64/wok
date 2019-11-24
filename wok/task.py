from datetime import datetime


class Task:

    isoformat = "%Y-%m-%dT%H:%M:%S.%f"

    def __init__(self, name):
        self.name = name
        self.datetimes = []
        self.current_datetime = []

    def start(self, dt=datetime.now()):
        if len(self.current_datetime) != 0:
            print(f"{self} already started")
            return False
        self.current_datetime.append(dt)
        print(f"{self} started at {self.current_datetime[0]}")
        return True

    def end(self, dt=datetime.now()):
        if len(self.current_datetime) != 1:
            print(f"{self} not yet started")
            return False
        self.current_datetime.append(dt)
        print(f"{self} ended at {self.current_datetime[1]}")
        duration = self.current_datetime[1] - self.current_datetime[0]
        print(
            f"\tDuration={duration}"
        )  # TODO format duration (type=timedelta) (use divmod)
        self.datetimes.append(self.current_datetime.copy())
        self.current_datetime.clear()
        return True

    def load(self, input):
        if len(self.current_datetime) > 1:
            print(f"ERR: {self} current datetime will be lost: {self.current_datetime}")
            self.current_datetime.clear()
        self.datetimes.clear()
        for line in input:
            if "->" in line:
                self.datetimes.append(
                    [datetime.strptime(x, Task.isoformat) for x in line.split("->")]
                )

    def save(self):
        if len(self.current_datetime) > 1:
            print(
                f"WARN: {self} current datetime will not be saved: {self.current_datetime}"
            )
        output = "\n".join(
            [
                "->".join([d.strftime(Task.isoformat) for d in dt])
                for dt in self.datetimes
            ]
        )
        return output

    def __str__(self):
        return f"Task '{self.name}'"
