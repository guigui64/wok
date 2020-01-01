import unittest
from datetime import datetime
from pathlib import Path

from wok.job import Job
from wok.task import Task
from wok.wok import Wok


class TestWok(unittest.TestCase):
    def setUp(self):
        # print("setting up test")
        pass

    # def test_run(self):
    #     # wok.run()
    #     self.assertTrue(True)

    # @unittest.skip
    # def test_skipped_test(self):
    #     self.assertTrue(False)

    # @unittest.expectedFailure
    # def test_failed_test(self):
    #     self.assertEqual(1, "2")

    def test_save_load(self):
        task1 = Task("task1")
        start = datetime(2019, 1, 10, 11, 11)
        end = datetime(2019, 1, 10, 11, 22)
        task1.start(dt=start)
        task1.end(dt=end)
        task2 = Task("task2")
        task3 = Task("task3")
        wok1 = Wok()
        job1 = Job("job1")
        wok1.jobs.append(job1)
        wok1.current_job_idx = 0
        job2 = Job("job2")
        wok1.jobs.append(job2)
        job1.add_task(task1)
        job1.add_task(task2)
        job2.add_task(task3)
        path = Path.cwd() / ".wok_test"
        wok1.save(dir=path)
        wok2 = Wok()
        wok2.load(dir=path)
        self.assertEqual(wok2.jobs[wok2.current_job_idx].name, "job1")
        self.assertEqual(len(wok2.jobs), 2)
        out = (path / "job1" / "task1").read_text()
        self.assertEqual(out, "2019-01-10T11:11:00.000000->2019-01-10T11:22:00.000000")

    def tearDown(self):
        # print("tearing down test")
        pass
