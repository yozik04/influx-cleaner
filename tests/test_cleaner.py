from unittest import TestCase

from influx_cleaner.cleaner import MeasurementEntry


class TestMeasurementEntry(TestCase):
    def test_repr(self):
        me = MeasurementEntry("test", {"time": 123, "value": 1})

        self.assertEqual("test\t123\t1", str(me))
        self.assertEqual("test\t123\t1", f"{me}")