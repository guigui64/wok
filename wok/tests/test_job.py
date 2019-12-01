import unittest

from wok.job import Job
from wok.task import Task


class TestJob(unittest.TestCase):
    def setUp(self):
        self.job = Job("tested_job")
        self.task = Task("task")

    def test_init(self):
        self.assertEqual(self.job.name, "tested_job")
        self.assertEqual(self.job.tasks, [])

    def test_add(self):
        self.assertTrue(self.job.add_task(self.task))
        self.assertEqual(self.job.get_task(self.task.name), self.task)

    def test_get_none(self):
        self.assertEqual(self.job.get_task("no_task"), None)

    def test_remove_task_name(self):
        self.job.add_task(self.task)
        self.assertTrue(self.job.remove_task_name(self.task.name))
        self.assertEqual(self.job.get_task(self.task.name), None)

    def test_remove_task(self):
        self.job.add_task(self.task)
        self.assertTrue(self.job.remove_task(self.task))
        self.assertEqual(self.job.get_task(self.task.name), None)
