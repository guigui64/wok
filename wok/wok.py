import pathlib

# from wok.job import Job
# from wok.task import Task


class Wok:

    default_dir = pathlib.Path.home() / ".wok"

    def __init__(self):
        self.jobs = []
        self.current_job = 0

    def __check_dir(dir):
        if dir.exists() and not dir.is_file():
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
        for file in dir.iterdir():
            pass  # TODO files and folders

    def save(self, dir=default_dir):
        if not self.__check_dir(dir):
            print("Could not save (see previous error)")
            return False
        # TODO save files
