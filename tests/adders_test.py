from circuits import adders, utils

import unittest


class TestAdders(unittest.TestCase):
    def test_half_adder(self):
        lines_map_in = utils.generate_line_map(2)
        lines_map_out = [[(False, False), (True, False), (True, False), (False, True)]]

        for line_out, *line_in_AB in zip(*lines_map_out, *lines_map_in):
            self.assertEqual(adders.half_adder(*line_in_AB), line_out)


if __name__ == "__main__":
    unittest.main()
