import argparse

from helpers import read_test, LEFT_MIRROR, RIGHT_MIRROR

class Laser:
    def __init__(self, orientation, position):
        self.orientation = orientation
        self.row = position[0]
        self.col = position[1]
        self.visited_cells = {position}  # set operations is more efficient than the list itself

    def move(self):
        """move the laser by one step"""
        self.row += self.orientation[0]
        self.col += self.orientation[1]
        self.visited_cells.add((self.row, self. col))

    def get_orientation(self):
        return self.orientation

    def set_orientation(self, new_orientation):
        self.orientation = new_orientation

    def get_position(self):
        return self.row, self.col

    def get_visited_cells(self):
        return self.visited_cells


class Cell:
    def __init__(self, mirror_type="None"):
        self.mirror_type = mirror_type

    def put_mirror(self, mirror_type):
        self.mirror_type = mirror_type

    def reflect(self, input_dir):
        if self.mirror_type == "right":
            new_dir = RIGHT_MIRROR[input_dir]
        elif self.mirror_type == "left":
            new_dir = LEFT_MIRROR[input_dir]
        elif self.mirror_type == "None":
            new_dir = input_dir
        return new_dir


class Grid:
    def __init__(self, rows, cols, joint_mirror_list):
        self.rows = rows
        self.cols = cols
        self.cells = []
        self.mirror_set = set()

        for i in range(self.rows):
            for j in range(self.cols):
                self.cells.append(Cell("None"))

        # iterate through the joint_mirror_list and change the mirror_type from default 'None'
        for mirror_tuple in joint_mirror_list:
            row, col, mirror_type = mirror_tuple
            row -= 1  # zero indexing to be consistent with Python
            col -= 1  # zero indexing to be consistent with Python
            index = row*self.cols + col
            current_cell = self.cells[index]
            current_cell.put_mirror(mirror_type)
            self.mirror_set.add((row, col)) # set operations is more efficient

    def compute_path(self, start_orientation, start_pos):
        """With the initialization of orientation and position, create a list of all visited cells"""
        beam = Laser(start_orientation, start_pos)
        current_position = beam.get_position()
        # it will stop if current position is out of grid, but since move() is executed after this condition,
        # points with one padding will be saved in visited_cells()
        while self.is_beam_inside(current_position):
            current_index = current_position[0]*self.cols + current_position[1]
            current_cell = self.cells[current_index]
            current_orientation = beam.get_orientation()
            new_orientation = current_cell.reflect(current_orientation)
            beam.set_orientation(new_orientation)
            beam.move()
            current_position = beam.get_position()

        return beam.get_visited_cells()

    def is_beam_inside(self, position):
        row, col = position
        row_inside = 0 <= row < self.rows
        col_inside = 0 <= col < self.cols
        return row_inside and col_inside

    def find_solutions(self):
        """output required results"""
        forward_path = self.compute_path((0, 1), (0, 0))
        backward_path = self.compute_path((0, -1), (self.rows-1, self.cols-1))
        # if the pint at (r-1,c) can be visited in forward_path, it means safe can be opened without inserting a mirror
        if (self.rows-1, self.cols) in forward_path:
            print(0)
            return

        intersection = forward_path.intersection(backward_path)
        intersection = intersection.difference(self.mirror_set) # only consider those overlaps where there doesn't exist a mirror already
        if not intersection:
            print("impossible")
            return
        else:
            # there are exactly k positions where inserting a mirror opens the safe
            num_solutions = len(intersection)
            # the lexicographically smallest such row, column position
            sorted_solutions = sorted(intersection)
            min_solution = sorted_solutions[0]
            print(num_solutions, min_solution[0] + 1, min_solution[1] + 1) # add 1 back
            return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file_name", help="Name of the test file", type=str)
    args = parser.parse_args()
    test_name = args.file_name
    total_rows, total_cols, joint_list = read_test(test_name)
    my_grid = Grid(total_rows, total_cols, joint_list)
    my_grid.find_solutions()
