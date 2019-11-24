import pathlib


class Wok:

    default_dir = pathlib.Path.home() / ".wok"

    def __init__(self):
        self.jobs = []
        self.current_job = 0

    def load(self, dir=default_dir):
        """ 
        for job_dir in dir.iterdir():
            job = Job(

        def list
        """
        pass
