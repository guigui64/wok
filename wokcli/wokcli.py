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
See 'wok <command> --help' for more help on each command"""
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
        job, task = self.wok.status()
        print("Current job:")
        print("\t" + job)
        print("\nCurrent task:")
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
        print("TODO job")

    def task(self):
        print("TODO task")

    def stat(self):
        print("TODO stat")


if __name__ == "__main__":
    WokCli()
