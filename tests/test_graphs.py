import os
import unittest

from apache_logs_parser.display import Graph

current_dir = os.path.dirname(os.path.realpath(__file__))


class TestGraphs(unittest.TestCase):
    def test_block_display(self):
        self.assertEqual(
            Graph.block(0),
            ''
        )
        self.assertEqual(
            Graph.block(1 / 8),
            '▏'
        )
        self.assertEqual(
            Graph.block(0.5),
            '▌'
        )
        self.assertEqual(
            Graph.block(1),
            '█'
        )

    def test_bars_display(self):
        self.assertEqual(
            Graph.horizontal_bar(0.5, 100),
            '▌'
        )

        self.assertEqual(
            Graph.horizontal_bar(1.5, 100),
            '█▌'
        )


if __name__ == '__main__':
    unittest.main()
