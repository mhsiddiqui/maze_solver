import unittest
from maze import Maze


class TestMazeWithCompletePathTillEnd(unittest.TestCase):
    def setUp(self):
        self.maze_data = {
            'size': (3, 3),
            'points': [34, 14, 12, 6, 77, 5, 1, 19, 9]
        }
        self.maze = Maze(**self.maze_data)

    def test_maze(self):
        assert ['up', 'up', 'left'] == \
               self.maze.solve_maze_and_return_directions(), 'Wrong Output'


class TestMazeWithNoPathTillEnd(unittest.TestCase):
    def setUp(self):
        self.maze_data = {
            'size': (3, 3),
            'points': [34, 18, 12, 6, 78, 9, 1, 19, 8]
        }
        self.maze = Maze(**self.maze_data)

    def test_maze(self):
        assert ['Maze is not Solvable'] == self.maze.solve_maze_and_return_directions(), 'Wrong Output'


if __name__ == '__main__':
    unittest.main()