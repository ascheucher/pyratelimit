import os
import yaml
from pyratelimit import PyRateLimit
from pyratelimit import PyRateLimitException
import unittest
import time

dirname, filename = os.path.split(os.path.abspath(__file__))
config = yaml.safe_load(open(r"{}/config.yaml".format(dirname)))

class TestRatePyLimit(unittest.TestCase):

    def test_exception(self):
        limit = PyRateLimit()
        self.assertRaises(PyRateLimitException,
                          limit.attempt, 'test_namespace')
        

    def test_throttle(self):
        PyRateLimit.init(redis_host=config['redis']['host'],
                         redis_port=config['redis']['port'])
        limit = PyRateLimit()
        limit.create(10,                    # rate limit period in seconds
                     10)                    # no of attempts in the time period

        for x in range(0, 20):
            time.sleep(.5)
            if x < 10:
                self.assertTrue(limit.attempt('test_namespace'))
            else:
                self.assertFalse(limit.attempt('test_namespace'))

        time.sleep(6)
        self.assertTrue(limit.attempt('test_namespace'))

    def test_peek(self):
        PyRateLimit.init(redis_host=config['redis']['host'],
                         redis_port=config['redis']['port'])
        limit = PyRateLimit()
        limit.create(10,                    # rate limit period in seconds
                     10)                    # no of attempts in the time period

        for _ in range(0, 10):
            time.sleep(0.5)
            self.assertTrue(limit.attempt('test_namespace2'))

        self.assertTrue(limit.is_rate_limited('test_namespace2'))
        time.sleep(10)
        self.assertFalse(limit.is_rate_limited('test_namespace2'))
