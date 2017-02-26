
UP = 1
RIGHT = 2
DOWN = 4
LEFT = 8
START = 16
END = 32
MINE = 64

LIVES = 3

ALL_ARRAY = [UP, RIGHT, DOWN, LEFT, START, END, MINE]


def get_all_mazes_from_file(file_name):
    """
    Read fine and return maze data
    :param file_name: File to be read
    :return: Maze list
    """
    maze_list = []
    with open(file_name, 'r') as f:
        content = filter(lambda x: x != '', f.read().split('\n'))
        for c in content:
            sp = c.split('-')
            dimensions = eval(sp[0])
            maze_points = eval(sp[1])
            maze = {
                'size': dimensions,
                'points': maze_points
            }
            maze_list.append(maze)
    return maze_list


class Maze(object):
    """
    Maze Solver Code
    """
    def __init__(self, size, points):
        self.i = 0
        self.size = size
        self.points = points
        self.chr_dict = {}
        self.start = None
        self.end = None

    def solve_maze_and_return_directions(self):
        chr_dict, start, end = self._get_all_points_characteristics()
        path = self.maze_solver(chr_dict, start, None, [], LIVES)
        coordinates = self.complete_path_coordinates(path)
        if ['Maze is not Solvable'] == coordinates:
            return ['Maze is not Solvable']
        else:
            directions = self.complete_path_directions(coordinates)
            return map(lambda x: x.lower(), directions)

    def complete_path_coordinates(self, path):
        """
        Get path from start to end from list of coordinates which has been traversed
        :return: Correct coordinates
        """
        correct_path = []
        if 'END' not in path:
            return ['Maze is not Solvable']
        else:
            for i in range(len(path)):
                if path[i] == 'END':
                    break
                if path[i] == 'MINE':
                    del correct_path[-1]
                else:
                    correct_path = self._delete_wrong_nodes(correct_path, i, path)
                    correct_path.append(path[i])
            return correct_path

    def complete_path_directions(self, correct_path):
        """
        Return complete path with direction like [Right, Left]
        :param correct_path: Coordinates of correct path
        :return: Directions
        """
        directions = []
        for j in range(1, len(correct_path)):
            direction = self._get_direction_from_points(correct_path[j], correct_path[j - 1])
            directions.append(direction)
        return directions

    def _delete_wrong_nodes(self, correct_path, index, path):
        """
        Delete wrong nodes from correct path. Wrong nodes are nodes which are in path when maze has two path
        one is correct and other is wrong and code traverse wrong first, all these wrong nodes will be in
        path list. This function will delete such nodes from path list.
        :param correct_path: Path list
        :param index: Current Index
        :return: Path list after deletion
        """

        all_neighbours = self._get_all_neighbours(path[index])
        while True:
            if bool(correct_path):
                if correct_path[-1] not in all_neighbours:
                    del correct_path[-1]
                else:
                    break
            else:
                break
        return correct_path

    def _get_all_neighbours(self, point):
        """
        Get all neighbours of current point
        :param point: Point whose neighbours are required
        :return: list of neighbours
        """
        all_neighbours = []
        for direction in ['UP', 'LEFT', 'DOWN', 'RIGHT']:
            all_neighbours.append(self._get_next_point(point, direction))
        return all_neighbours

    def _get_direction_from_points(self, current, previous):
        """
        Return direction of current point from previous point i.e. right ot left
        :param current: Current point
        :param previous: Previous point
        :return: direction i.e. Right
        """
        if current and previous and not isinstance(current, str):
            if [current[0] + 1, current[1]] == previous:
                return 'UP'
            elif [current[0] - 1, current[1]] == previous:
                return 'DOWN'
            elif [current[0], current[1] + 1] == previous:
                return 'LEFT'
            elif [current[0], current[1] - 1] == previous:
                return 'RIGHT'
        return

    def _get_all_points_characteristics(self):
        """
        Make dictionary of characteristics of all points and store them according to coordinates.
        Alse set start and end point of maze
        :return: characteristics dict, start and end point
        """
        chr_dict = {}
        start = []
        end = []
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                characteristics = self._extract_cell_characteristics(self.points[self.size[1] * x + y])
                if START in characteristics:
                    start = [x, y]
                if END in characteristics:
                    end = [x, y]
                tmp = {
                    'value': self.points[self.size[1] * x + y],
                    'coordinates': [x, y],
                    'UP': UP in characteristics,
                    'RIGHT': RIGHT in characteristics,
                    'DOWN': DOWN in characteristics,
                    'LEFT': LEFT in characteristics,
                    'START': START in characteristics,
                    'END': END in characteristics,
                    'MINE': MINE in characteristics
                }
                chr_dict.update({'%s-%s' % (x, y): tmp})
        return chr_dict, start, end

    def _extract_cell_characteristics(self, cell_value):
        """
        Return cell characteristics by value. Like if value is 74, then it will return 64, 8, 2
        :param cell_value: Integer like 74
        :return: list of integer like [64, 8, 2]
        """
        ch_list = []
        for coin_val in sorted(ALL_ARRAY, reverse=True):
            coin_count = cell_value / coin_val
            ch_list += [coin_val, ] * coin_count
            cell_value -= coin_val * coin_count
        return ch_list

    def _get_characteristics_by_point(self, point, characteristics_dict):
        """
        Get point characteristics from characteristics dictionary
        :param point: Point whose characteristics are required
        :return: characteristics
        """
        return characteristics_dict.get('%s-%s' % tuple(point))

    def maze_solver(self, characteristics_dict, current_point, previous, path, lives):
        """
        Maze Solver Recursive code
        :param current_point: Current Point
        :param previous: Previous point
        :param path: Path which has been traversed
        :param lives: Lives remaining
        :return: Complete traversed path from start to end
        """
        point_characteristics = self._get_characteristics_by_point(current_point, characteristics_dict)
        path.append(current_point)
        if point_characteristics.get('MINE'):
            lives -= 1
            if lives == 0:
                return path + ['MINE']
        if point_characteristics.get('END'):
            return path + ['END']
        for direction in ['UP', 'LEFT', 'DOWN', 'RIGHT']:
                if point_characteristics.get(direction):
                    next_point = self._get_next_point(current_point, direction)
                    if next_point != previous:
                        if not next_point in path:
                            path = self.maze_solver(characteristics_dict, next_point, current_point, path, lives)
        return path

    def _get_next_point(self, point, position):
        """
        Return Next point on the basis of provided direction
        :param point: Coordinates of point. i.e. [2,3]
        :param position: Direction in which you want to get next point like 'UP
        :return: Next point in required direction
        """
        next_point = []
        if position == 'UP':
            next_point = [point[0] - 1, point[1]]
        elif position == 'DOWN':
            next_point = [point[0] + 1, point[1]]
        elif position == 'LEFT':
            next_point = [point[0], point[1] - 1]
        elif position == 'RIGHT':
            next_point = [point[0], point[1] + 1]
        return next_point

if __name__ == '__main__':

    while True:
        command = raw_input('File Name With Complete Path (Type Q To Quit) >> ')
        if command.lower() == 'q':
            print 'Good Bye'
            break
        else:
            maze_list = get_all_mazes_from_file('mazes.txt')
            print '%s Maze(s) found In file' % len(maze_list)
            index = 1
            for maze_data in maze_list:
                print 'Maze # %s' % index
                maze = Maze(**maze_data)
                print maze.solve_maze_and_return_directions()
                print '------'
                index += 1







