import unittest


from inspector.collectors.env import EnvDataCollector
from inspector.commons.context import Context


class EnvTest(unittest.TestCase):

    def test_snapshot(self):
        env = EnvDataCollector(Context(name="test"))
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
        self.assert_non_empty_key(bazel_info, "real_path")
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

    def assert_non_empty_key(self, dictionary, key):
        self.assertTrue(key in dictionary, "key \"%s\" does not exist" % key)
        self.assertIsNotNone(dictionary[key], "the value of \"%s\" is None" % key)


if __name__ == '__main__':
    unittest.main()
