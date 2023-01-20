from circuits import gates

import unittest


class TestTransistor(unittest.TestCase):
    def test_out(self):
        self.assertEqual(gates.transistor(True, True), True)


if __name__ == "__main__":
    unittest.main()
