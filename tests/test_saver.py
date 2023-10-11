import unittest

from shedule_manager.schedule_saver import refresh_schedule


class TestSaver(unittest.TestCase):

    def test_refresh_schedule(self):
        refresh_schedule()