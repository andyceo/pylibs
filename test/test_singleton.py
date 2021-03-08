import unittest
from singleton import Singleton


class ThisIsSingleton(metaclass=Singleton):
    pass


class ThisIsNotSingleton:
    pass


class TestSingleton(unittest.TestCase):
    def test_singleton(self):
        s1 = ThisIsSingleton()
        self.assertIsNotNone(s1)

        s2 = ThisIsSingleton()
        self.assertIsNotNone(s2)

        self.assertEqual(s1, s2)

        s3 = ThisIsNotSingleton()
        self.assertIsNotNone(s3)

        s4 = ThisIsNotSingleton()
        self.assertIsNotNone(s4)

        self.assertNotEqual(s3, s4)
