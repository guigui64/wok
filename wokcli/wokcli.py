import sys
from argparse import ArgumentParser, RawDescriptionHelpFormatter

from wok.api import WokApi


class WokCli:
    def __init__(self):
        self.api = WokApi()
        self.api.load()
        self.save = False
        self.run()
        if self.save:
            self.api.save()

    def run(self):
        parser = ArgumentParser(
            epilog="""Available commands are:
* status  : display current job and running task(s)
* switch  : switch between jobs
* job     : handle jobs (list, create, delete, ...)
* task    : handle tasks (list, create, delete, ...)
* end     : suspend a task or all running tasks if any
* start   : start the given task (can be prefixed by job name 'job.task')
* details : display detailed tables of all jobs and tasks
See 'wok <command> --help' for more help on each command""",
            formatter_class=RawDescriptionHelpFormatter,
        )
        parser.add_argument(
            "command",
            choices=["status", "switch", "job", "task", "end", "start", "details"],
            nargs="?",
            default="status",
        )
        args = parser.parse_args(sys.argv[1:2])
        # Invoke method with command name
        getattr(self, args.command)()

    def status(self):
        parser = ArgumentParser(
            prog=sys.argv[0] + " status",
            description="Display current job and running task(s)",
        )
        parser.parse_args()
        res, out = self.api.status()
        if res:
            print(out)

    def switch(self):
        parser = ArgumentParser(
            prog=sys.argv[0] + " switch", description="Switch to a job"
        )
        parser.add_argument("job", help="the job to switch to")
        parser.add_argument(
            "-c",
            "--create",
            action="store_true",
            help="Create the job if it does not exist",
        )
        args = parser.parse_args(sys.argv[2:])
        self.save, out = self.api.switch(args.job, create=args.create)
        print(out)

    def start(self):
        parser = ArgumentParser(prog=sys.argv[0] + " start", description="Start a task")
        parser.add_argument(
            "path",
            help="the task to start, can be prefixed by the job as 'job.task'",
            nargs="*",
        )
        parser.add_argument(
            "-c",
            "--create",
            action="store_true",
            help="Create the task if it does not exist",
        )
        args = parser.parse_args(sys.argv[2:])
        for path in args.path:
            started, out = self.api.start(path, create=args.create)
            if started:
                # One task started might be False but save must stay True
                self.save = True
            print(out)

    def end(self):
        parser = ArgumentParser(
            prog=sys.argv[0] + " end",
            description="Suspend a task or all running tasks if any",
        )
        parser.add_argument(
            "path",
            help="the task to end, can be prefixed by the job as 'job.task'",
            nargs="*",
        )
        args = parser.parse_args(sys.argv[2:])
        if len(args.path) == 0:
            self.save, out = self.api.suspend()
            print(out)
        else:
            for path in args.path:
                res, msg = self.api.end(path)
                if res:
                    # One task res might be False but save must stay True
                    self.save = True
                print(msg)

    def __check_args_nb(self, li, fun):
        if not fun(len(li)):
            print("Incorrect number of arguments")
            return False
        return True

    def job(self):
        description = "Handle jobs\n\n"
        description += "Examples:\n"
        description += f"\t- '{sys.argv[0]} job my_job' : display info about 'my_job'\n"
        description += f"\t- '{sys.argv[0]} job --create my_other_job'\n"
        description += f"\t- '{sys.argv[0]} job --rename my_other_job my_newer_job'"
        parser = ArgumentParser(
            prog=sys.argv[0] + " job",
            description=description,
            formatter_class=RawDescriptionHelpFormatter,
        )
        parser.add_argument(
            "-t",
            "--table",
            action="store_true",
            help="Display jobs details in table format",
        )
        group = parser.add_mutually_exclusive_group()
        group.add_argument(
            "-c", "--create", action="store_true", help="Create a job",
        )
        group.add_argument(
            "-d",
            "--delete",
            action="store_true",
            help="Delete the specified job and all its tasks",
        )
        group.add_argument(
            "-r", "--rename", action="store_true", help="Rename the specified job"
        )
        group.add_argument(
            "-l", "--list", action="store_true", help="List all existing jobs"
        )
        parser.add_argument("job", nargs="*", help="The job(s) to handle")
        args = parser.parse_args(sys.argv[2:])
        if args.create:
            if not self.__check_args_nb(args.job, lambda x: x > 0):
                return
            for job in args.job:
                res, msg = self.api.add_job(job)
                if res:
                    # One job res might be False but save must stay True
                    self.save = True
                print(msg)
        elif args.delete:
            if not self.__check_args_nb(args.job, lambda x: x == 1):
                return
            self.save, out = self.api.delete_job(args.job[0])
            print(out)
        elif args.rename:
            if not self.__check_args_nb(args.job, lambda x: x == 2):
                return
            self.save, out = self.api.rename_job(*args.job[:2])
            print(out)
        elif len(args.job) == 0 or args.list:
            _, out = self.api.list_jobs()
            print(out)
        else:
            for job in args.job:
                _, out = self.api.get_job_details(job, table=args.table)
                print(out)

    def task(self):
        description = "Handle tasks\n\n"
        description += "Examples:\n"
        description += (
            f"\t- '{sys.argv[0]} task my_task' : display info about 'my_task'\n"
        )
        description += f"\t- '{sys.argv[0]} task --create my_other_task'\n"
        description += f"\t- '{sys.argv[0]} task --rename my_other_task my_newer_task'"
        parser = ArgumentParser(
            prog=sys.argv[0] + " task",
            description=description,
            formatter_class=RawDescriptionHelpFormatter,
        )
        parser.add_argument(
            "-t",
            "--table",
            action="store_true",
            help="Display tasks details in table format",
        )
        group = parser.add_mutually_exclusive_group()
        group.add_argument(
            "-c",
            "--create",
            action="store_true",
            help="Create a task in the current job",
        )
        group.add_argument(
            "-d", "--delete", action="store_true", help="Delete the specified task",
        )
        group.add_argument(
            "-r", "--rename", action="store_true", help="Rename the specified task"
        )
        group.add_argument(
            "-l",
            "--list",
            action="store_true",
            help="List all existing tasks in the current job",
        )
        parser.add_argument("task", nargs="*", help="The task(s) to handle")
        args = parser.parse_args(sys.argv[2:])
        if args.create:
            if not self.__check_args_nb(args.task, lambda x: x > 0):
                return
            for task in args.task:
                res, msg = self.api.add_task(task)
                if res:
                    # One task res might be False but save must stay True
                    self.save = True
                print(msg)
        elif args.delete:
            if not self.__check_args_nb(args.task, lambda x: x == 1):
                return
            self.save, out = self.api.delete_task(args.task[0])
            print(out)
        elif args.rename:
            if not self.__check_args_nb(args.task, lambda x: x == 2):
                return
            self.save, out = self.api.rename_task(*args.task[:2])
            print(out)
        elif len(args.task) == 0 or args.list:
            _, out = self.api.list_current_job_tasks()
            print(out)

        else:
            for task in args.task:
                _, out = self.api.get_task_details(task, table=args.table)
                print(out)

    def details(self):
        parser = ArgumentParser(
            prog=sys.argv[0] + " details",
            description="Display detailed tables of all jobs and tasks",
        )
        parser.parse_args()
        _, out = self.api.get_details()
        print(out)


def main():
    WokCli()


if __name__ == "__main__":
    main()
