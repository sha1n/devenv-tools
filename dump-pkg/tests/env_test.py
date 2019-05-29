import sys
import unittest

from dump.env import EnvDataCollector
from tests.testutil import test_context


@unittest.skipUnless(sys.platform == "darwin", "requires MacOS")
class EnvTest(unittest.TestCase):

    def test_snapshot(self):
        env = EnvDataCollector(test_context(), "", "")
        snapshot = env.snapshot()
        self.assertIsNotNone(snapshot)
        self.assert_non_empty_key(snapshot, "timestamp_utc")
        self.assert_non_empty_key(snapshot, "user")
        self.assert_non_empty_key(snapshot, "hostname")
        self.assert_non_empty_key(snapshot, "cpu_count")
        self.assert_non_empty_key(snapshot, "total_ram")

        self.assert_non_empty_key(snapshot, "os")
        os_info = snapshot["os"]
        self.assert_non_empty_key(os_info, "name")
        self.assert_non_empty_key(os_info, "version")

        self.assert_non_empty_key(snapshot, "bazel")
        bazel_info = snapshot["bazel"]
        self.assert_non_empty_key(bazel_info, "path")
        self.assert_non_empty_key(bazel_info, "bazelisk")
        self.assert_non_empty_key(bazel_info, "version")

        self.assert_non_empty_key(snapshot, "python")
        python_info = snapshot["python"]
        self.assert_non_empty_key(python_info, "version")

        self.assert_non_empty_key(snapshot, "disk")
        disk_info = snapshot["disk"]
        self.assert_non_empty_key(disk_info, "filesystem")
        self.assert_non_empty_key(disk_info, "free")
        self.assert_non_empty_key(disk_info, "used")
        self.assert_non_empty_key(disk_info, "total")

        self.assert_non_empty_key(snapshot, "gcloud")
        gcloud_info = snapshot["gcloud"]
        self.assert_non_empty_key(gcloud_info, "configured")

        self.assert_non_empty_key(snapshot, "docker")
        docker_info = snapshot["docker"]
        self.assert_non_empty_key(docker_info, "configured")
        self.assert_non_empty_key(docker_info, "running")

        self.assert_non_empty_key(snapshot, "network")
        network_info = snapshot["network"]
        self.assert_non_empty_key(network_info, "connectivity_checks")

    def assert_non_empty_key(self, dictionary, key):
        self.assertTrue(key in dictionary, "key \"%s\" does not exist" % key)
        self.assertIsNotNone(dictionary[key], "the value of \"%s\" is None" % key)


if __name__ == '__main__':
    unittest.main()
