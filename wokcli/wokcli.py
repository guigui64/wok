import argparse
import sys

from wok import wok


class WokCli:
    def __init__(self):
        self.__loadWok()
        self.__run()
        self.__saveWok()

    def __loadWok(self):
        self.wok = wok.Wok()
        self.wok.load()

    def __saveWok(self):
        self.wok.save()

    def __run(self):
        parser = argparse.ArgumentParser(
            epilog="""TODO list available commands
See 'wok <command> --help' for more help on each command""",
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )
        parser.add_argument(
            "command",
            choices=["status", "switch", "suspend", "job", "task", "stat"],
            nargs="?",
            default="status",
        )
        args = parser.parse_args(sys.argv[1:2])
        # Invoke method with command name
        getattr(self, args.command)()

    def status(self):
        job, tasks = self.wok.status()
        print("Current job:")
        print("\t" + job)
        print("\nRunning task(s):")
        for task in tasks:
            print("\t" + task)

    def switch(self):
        parser = argparse.ArgumentParser(
            prog=sys.argv[0] + " switch", description="Switch to a job"
        )
        parser.add_argument("job", help="the job to switch to")
        parser.add_argument("-c", "--create", action="store_true")
        args = parser.parse_args(sys.argv[2:])
        if self.wok.switch(args.job, create=args.create):
            print(f"Switched to job {args.job}")
        else:
            print(f"Impossible to switch to job {args.job}, try using the '-c' option")

    def suspend(self):
        if self.wok.suspend():
            print("Task(s) suspended")
        else:
            print("No task to suspend")

    def job(self):
        description = "Handle jobs\n\n"
        description += "Examples:\n"
        description += f"\t- '{sys.argv[0]} job my_job' : display info about 'my_job'\n"
        description += f"\t- '{sys.argv[0]} job --create my_other_job'\n"
        description += f"\t- '{sys.argv[0]} job --rename my_other_job my_newer_job'"
        parser = argparse.ArgumentParser(
            prog=sys.argv[0] + " job",
            description=description,
            formatter_class=argparse.RawDescriptionHelpFormatter,
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
        parser.add_argument("job", nargs="*")
        args = parser.parse_args(sys.argv[2:])
        if args.list:
            jobs, current = self.wok.get_jobs()
            for i, j in enumerate(jobs):
                if i == current:
                    print(j.name + " [current]")
                else:
                    print(j.name)
        elif args.create:
            for job in args.job:
                res, msg = self.wok.add_job(job)
                if res:
                    print(f"Job '{job}' created")
                else:
                    print(msg)
        elif args.delete:
            if self.wok.delete_job(args.job[0]):
                print(f"Job '{args.job[0]}' deleted!")
            else:
                print(f"No job '{args.job[0]}' found to delete")
        elif args.rename:
            job = self.wok.get_job(args.job[0])
            if job is None:
                print(f"Could not rename job '{args.job[0]}'")
            else:
                job.name = args.job[1]
                print(f"Job '{args.job[0]}' renamed '{args.job[1]}' successfully")
        else:
            for job in args.job:
                print(self.wok.get_job(job))

    def task(self):
        print("TODO task")

    def stat(self):
        print("TODO stat")


if __name__ == "__main__":
    WokCli()
