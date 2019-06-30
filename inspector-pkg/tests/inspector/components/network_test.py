import unittest

from inspector.components.network import UrlConnectivityInfoCollector
from tests.testutil import test_context


class UrlConnectivityInfoCollectorTest(unittest.TestCase):

    def test_missing_config(self):
        collector = UrlConnectivityInfoCollector()

        result = collector.collect(ctx=context_with_no_netwoek_config())
        self.assertEqual(0, len(result))

    def test_empty(self):
        collector = UrlConnectivityInfoCollector()

        result = collector.collect(ctx=context_with_empty_net_checks())
        self.assertEqual(0, len(result))

    def test_failure(self):
        collector = UrlConnectivityInfoCollector()

        result = collector.collect(ctx=context_with_unavailable_address())

        self.assertEqual(1, len(result))
        self.assertFalse(result[0].ok)
        self.assertGreaterEqual(result[0].time, 0)


def context_with_empty_net_checks():
    ctx = test_context()
    ctx.config = {
        "network": {
            "check_specs": []
        }
    }
    return ctx


def context_with_no_netwoek_config():
    ctx = test_context()
    ctx.config = {}

    return ctx


def context_with_unavailable_address():
    from uuid import uuid4
    ctx = test_context()
    ctx.config = {
        "network": {
            "check_specs": [
                {
                    "address": "http://localhost/{}".format(uuid4()),
                    "failure_message": "dummy"
                }
            ]
        }
    }

    return ctx


if __name__ == '__main__':
    unittest.main()
