import unittest
from src.str8ts import Str8ts, get_next_pos_with_least, NoSolutionPossibleException


class MyTestCase(unittest.TestCase):
    empty_board_numbers_3x3 = {(0, 0): None, (0, 1): None, (0, 2): None, (1, 0): None, (1, 1): None, (1, 2): None,
                               (2, 0): None,
                               (2, 1): None, (2, 2): None, }

    def test_board_numbers(self):
        str8ts = Str8ts(3, 3)
        self.assertDictEqual(str8ts.board_numbers, self.empty_board_numbers_3x3)

    def test_board_blocks(self):
        str8ts = Str8ts(3, 3)
        self.assertListEqual(str8ts.board_blocks, list())

    def test_possibilities(self):
        str8ts = Str8ts(3, 3)
        expected = [1, 2, 3]
        self.assertListEqual(str8ts.possilities_per_field, expected)

    def test_insert_board_1(self):
        str8ts = Str8ts(3, 3)
        str8ts.insert_fields()
        self.assertDictEqual(str8ts.board_numbers, self.empty_board_numbers_3x3)
        self.assertListEqual(str8ts.board_blocks, list())

    def test_insert_board_2(self):
        str8ts = Str8ts(3, 3)
        str8ts.insert_fields({(0, 0): 1, (0, 2): 2, (2, 1): 3})
        self.assertDictEqual(str8ts.board_numbers,
                             {(0, 0): 1, (0, 1): None, (0, 2): 2,
                              (1, 0): None, (1, 1): None, (1, 2): None,
                              (2, 0): None, (2, 1): 3, (2, 2): None, })

    def test_insert_board_3(self):
        str8ts = Str8ts(3, 3)
        str8ts.insert_fields(blocks=[(2, 2), ])
        self.assertListEqual(str8ts.board_blocks, [(2, 2)])

    def test_get_whole_x_line_1(self):
        str8ts = Str8ts(9, 9)
        str8ts.insert_fields()
        x_line = str8ts.get_whole_x_line((2, 3))
        self.assertListEqual(x_line, [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8)])

    def test_get_whole_x_line_2(self):
        str8ts = Str8ts(9, 9)
        str8ts.insert_fields(blocks=[(2, 1), (2, 2), (2, 7), (3, 3), (4, 2)])
        x_line = str8ts.get_whole_x_line((2, 3))
        self.assertListEqual(x_line, [(2, 0), (2, 3), (2, 4), (2, 5), (2, 6), (2, 8)])

    def test_get_whole_y_line_1(self):
        str8ts = Str8ts(9, 9)
        str8ts.insert_fields()
        x_line = str8ts.get_whole_x_line((2, 3))
        self.assertListEqual(x_line, [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8)])

    def test_get_whole_y_line_2(self):
        str8ts = Str8ts(9, 9)
        str8ts.insert_fields(blocks=[(2, 1), (2, 2), (2, 7), (3, 3), (4, 2)])
        y_line = str8ts.get_whole_y_line((2, 3))
        self.assertListEqual(y_line, [(0, 3), (1, 3), (2, 3), (4, 3), (5, 3), (6, 3), (7, 3), (8, 3)])

    def test_get_small_x_line_1(self):
        str8ts = Str8ts(9, 9)
        str8ts.insert_fields(blocks=[(2, 1), (2, 2), (2, 7), (3, 3), (4, 2)])
        x_line_small = str8ts.get_small_x_line((2, 3))
        self.assertListEqual(x_line_small, [(2, 3), (2, 4), (2, 5), (2, 6)])

    def test_get_small_x_line_2(self):
        str8ts = Str8ts(9, 9)
        str8ts.insert_fields(blocks=[(2, 1), (2, 2), (2, 7), (3, 3), (4, 2)])
        x_line_small = str8ts.get_small_x_line((2, 0))
        self.assertListEqual(x_line_small, [(2, 0)])

    def test_get_small_y_line_1(self):
        str8ts = Str8ts(9, 9)
        str8ts.insert_fields(blocks=[(2, 1), (2, 2), (2, 7), (3, 3), (4, 2)])
        x_line_small = str8ts.get_small_y_line((1, 2))
        x_line_small.sort()
        self.assertListEqual(x_line_small, [(0, 2), (1, 2)])

    def test_get_small_y_line_2(self):
        str8ts = Str8ts(9, 9)
        str8ts.insert_fields(blocks=[(2, 1), (2, 2), (2, 7), (3, 3), (4, 2)])
        x_line_small = str8ts.get_small_y_line((2, 0))
        x_line_small.sort()
        self.assertListEqual(x_line_small, [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0)])

    def test_get_next_pos_with_least_1(self):
        wave = {(0, 0): [1, 2, 3], (0, 3): [2], (0, 4): [4]}
        posibilities = get_next_pos_with_least(wave)
        self.assertListEqual(posibilities, [(0, 3), (0, 4)])

    def test_get_next_pos_with_least_2(self):
        wave = {(0, 0): [1, 2, 3], (0, 3): [], (0, 4): []}
        with self.assertRaises(NoSolutionPossibleException):
            posibilities = get_next_pos_with_least(wave)

    def test_get_solution_1(self):
        str8ts = Str8ts(6, 6)
        str8ts.insert_fields(
            inputs={(3, 0): 6, (0, 1): 6, (4, 1): 2, (2, 2): 5, (5, 2): 4, (4, 3): 4, (2, 4): 1, (4, 4): 6},
            blocks=[(2, 0), (3, 0), (0, 2), (1, 2), (2, 2), (1, 3), (4, 3), (5, 3), (0, 5), (3, 5)])
        solution = {(0, 0): 5, (0, 1): 6, (0, 2): 0, (0, 3): 1, (0, 4): 2, (0, 5): 0,
                    (1, 0): 4, (1, 1): 5, (1, 2): 0, (1, 3): 0, (1, 4): 3, (1, 5): 2,
                    (2, 0): 0, (2, 1): 4, (2, 2): 5, (2, 3): 2, (2, 4): 1, (2, 5): 3,
                    (3, 0): 6, (3, 1): 1, (3, 2): 2, (3, 3): 3, (3, 4): 4, (3, 5): 0,
                    (4, 0): 1, (4, 1): 2, (4, 2): 3, (4, 3): 4, (4, 4): 6, (4, 5): 5,
                    (5, 0): 2, (5, 1): 3, (5, 2): 4, (5, 3): 0, (5, 4): 5, (5, 5): 6, }
        self.assertDictEqual(str8ts.get_solution(), solution)

    def test_get_solution_2(self):
        str8ts = Str8ts(6, 6)
        str8ts.insert_fields(
            inputs={(0, 0): 1, (1, 4): 6, (2, 3): 3, (3, 0): 6, (3, 2): 5, (4, 3): 1, (5, 5): 3},
            blocks=[(0, 2), (0, 5), (1, 4),(1,5), (2, 0), (4, 4), (4, 5), (5, 2), (5, 5)])
        solution = {(0, 0): 1, (0, 1): 2, (0, 2): 0, (0, 3): 6, (0, 4): 5, (0, 5): 0,
                    (1, 0): 2, (1, 1): 4, (1, 2): 3, (1, 3): 5, (1, 4): 6, (1, 5): 0,
                    (2, 0): 0, (2, 1): 5, (2, 2): 4, (2, 3): 3, (2, 4): 3, (2, 5): 2,
                    (3, 0): 6, (3, 1): 1, (3, 2): 5, (3, 3): 4, (3, 4): 3, (3, 5): 2,
                    (4, 0): 4, (4, 1): 3, (4, 2): 2, (4, 3): 1, (4, 4): 0, (4, 5): 0,
                    (5, 0): 5, (5, 1): 6, (5, 2): 0, (5, 3): 2, (5, 4): 1, (5, 5): 3, }
        self.assertDictEqual(str8ts.get_solution(), solution)


if __name__ == '__main__':
    unittest.main()
