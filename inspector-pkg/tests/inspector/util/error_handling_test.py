import unittest

from shminspector.util.error_handling import try_wrap, raised_to_none_wrapper


class ErrorsTest(unittest.TestCase):

    def test_try_wrap_with_error(self):
        result, error = self.try_wrapped_error()
        self.assertIsNone(result)
        self.assertIsNotNone(error)

    def test_try_wrap_with_no_error(self):
        result, error = self.try_wrapped_no_error()
        self.assertIsNone(error)
        self.assertIsNotNone(result)

    def test_raised_to_none_with_error(self):
        self.assertIsNone(raised_to_none_wrapper(self.error)())

    def test_raised_to_none_with_no_error(self):
        self.assertEqual("ok", raised_to_none_wrapper(self.no_error)())

    def error(self):
        raise Exception("Fake error")

    def no_error(self):
        return "ok"

    @try_wrap
    def try_wrapped_error(self):
        return self.error()

    @try_wrap
    def try_wrapped_no_error(self):
        return self.no_error()


if __name__ == '__main__':
    unittest.main()
