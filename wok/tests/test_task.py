import unittest
from datetime import datetime

from wok.task import Task


class TestTask(unittest.TestCase):
    def setUp(self):
        self.task = Task("tested_task")

    def test_init(self):
        self.assertEqual(self.task.name, "tested_task")
        self.assertEqual(self.task.datetimes, [])
        self.assertFalse(self.task.is_running())

    def test_start(self):
        now = datetime.now()
        res = self.task.start(dt=now)
        self.assertTrue(res)
        self.assertEqual(self.task.current_datetime, now)
        self.assertTrue(self.task.is_running())

    def test_start_twice(self):
        now = datetime.now()
        res = self.task.start(dt=now)
        self.assertTrue(res)
        self.assertTrue(self.task.is_running())
        res, _ = self.task.start(dt=now)
        self.assertFalse(res)

    def test_end(self):
        res, _ = self.task.end()
        self.assertFalse(res)
        self.assertFalse(self.task.is_running())

    def test_start_end_save(self):
        start = datetime(2019, 1, 10, 11, 11)
        end = datetime(2019, 1, 10, 11, 22)
        self.task.start(dt=start)
        self.task.end(dt=end)
        self.assertEqual(self.task.datetimes, [(start, end)])
        self.assertEqual(self.task.current_datetime, None)
        out = self.task.save()
        self.assertEqual(out, "2019-01-10T11:11:00.000000->2019-01-10T11:22:00.000000")
        start2 = datetime(2019, 1, 10, 11, 23)
        self.task.start(dt=start2)
        self.assertEqual(self.task.datetimes, [(start, end)])
        self.assertEqual(self.task.current_datetime, start2)
        out = self.task.save()
        self.assertEqual(
            out,
            "2019-01-10T11:11:00.000000->2019-01-10T11:22:00.000000\nC:2019-01-10T11:23:00.000000",
        )

    def test_load(self):
        start = datetime(2019, 1, 10, 11, 11)
        end = datetime(2019, 1, 10, 11, 22)
        self.task.load(["2019-01-10T11:11:00.000000->2019-01-10T11:22:00.000000"])
        self.assertEqual(self.task.datetimes, [(start, end)])
        self.assertEqual(self.task.current_datetime, None)
