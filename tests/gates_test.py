from circuits import gates, utils

import unittest


class TestGates(unittest.TestCase):
    def test_gate_not(self):
        lines_map_in = utils.generate_line_map(1)
        lines_map_out = [[True, False]]

        for line_in, line_out in zip(*lines_map_in, *lines_map_out):
            self.assertEqual(gates.gate_not(line_in), line_out)

    def test_gate_and(self):
        lines_map_in = utils.generate_line_map(2)
        lines_map_out = [[False, False, False, True]]

        for line_out, *line_in_AB in zip(*lines_map_out, *lines_map_in):
            self.assertEqual(gates.gate_and(line_in_AB), line_out)

        lines_map_in = utils.generate_line_map(3)
        lines_map_out = [[False, False, False, False, False, False, False, True]]

        for line_out, *line_in_AB in zip(*lines_map_out, *lines_map_in):
            self.assertEqual(gates.gate_and(line_in_AB), line_out)

    def test_gate_or(self):
        lines_map_in = utils.generate_line_map(2)
        lines_map_out = [[False, True, True, True]]

        for line_out, *line_in_AB in zip(*lines_map_out, *lines_map_in):
            self.assertEqual(gates.gate_or(line_in_AB), line_out)

        lines_map_in = utils.generate_line_map(3)
        lines_map_out = [[False, True, True, True, True, True, True, True, True]]

        for line_out, *line_in_AB in zip(*lines_map_out, *lines_map_in):
            self.assertEqual(gates.gate_or(line_in_AB), line_out)

    def test_gate_nand(self):
        lines_map_in = utils.generate_line_map(2)
        lines_map_out = [[True, True, True, False]]

        for line_out, *line_in_AB in zip(*lines_map_out, *lines_map_in):
            self.assertEqual(gates.gate_nand(line_in_AB), line_out)

        lines_map_in = utils.generate_line_map(3)
        lines_map_out = [[True, True, True, True, True, True, True, False]]

        for line_out, *line_in_AB in zip(*lines_map_out, *lines_map_in):
            self.assertEqual(gates.gate_nand(line_in_AB), line_out)

    def test_gate_xor(self):
        lines_map_in = utils.generate_line_map(2)
        lines_map_out = [[False, True, True, False]]

        for line_out, *line_in_AB in zip(*lines_map_out, *lines_map_in):
            self.assertEqual(gates.gate_xor(*line_in_AB), line_out)


if __name__ == "__main__":
    unittest.main()
