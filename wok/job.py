class Job:
    """A Job has a name and a list of tasks."""

    def __init__(self, name):
        self.name = name
        self.tasks = []

    def add_task(self, task):
        """Adds the task if the name is not taken

        :param task: The task to add
        :type task: Task
        :return: True for success
        :rype: boolean

        """
        if self.__get_task(task.name):
            print(f"A task with name '{task.name}' already exists in job {self.name}")
            return False
        self.tasks.append(task)
        return True

    def remove_task(self, task):
        """

        :param task: The task to remove
        :type task: Task
        :return: True for success
        :rtype: boolean

        """
        try:
            self.tasks.remove(task)
            return True
        except ValueError:
            return False

    def __get_task(self, taskname):
        """Inner get_task with no log"""
        try:
            return next(filter(lambda t: t.name == taskname, self.tasks))
        except StopIteration:
            return None

    def get_task(self, taskname):
        """

        :param taskname: The name of the task to get
        :type taskname: string
        :return: the task or None if not found
        :rtype: Task

        """
        task = self.__get_task(taskname)
        if not task:
            print(f"No task with name '{taskname}' found in job {self.name}")
        return task

    def remove_task_name(self, taskname):
        """

        :param taskname: The name of the task to remove
        :type taskname: string
        :return: True for success
        :rtype: boolean

        """
        return self.remove_task(self.get_task(taskname))

    def load(self, input):
        """Loads the job from the content of its file

        :param input: The content of its file
        :type input: [string]
        :return: True for success
        :rtype: boolean

        """
        pass  # TODO load

    # TODO save

    def __str__(self):
        s = f"Job '{self.name}'\n"
        for task in self.tasks:
            s += f"\t{task}\n"
        return s[:-1]  # Remove last \n
