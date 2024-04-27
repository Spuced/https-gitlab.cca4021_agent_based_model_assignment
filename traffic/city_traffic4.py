import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Car:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction
        self.move_plan = []

    def plan_moves(self, grid):
        row, col = self.position
        n_rows, n_cols = grid.shape
        if not self.move_plan:
            if grid[row, col] == 2:  # At an intersection
                action = np.random.choice(['straight', 'left', 'right'])
                if action == 'straight':
                    self.move_plan = [self.direction] * 3
                elif action == 'left':
                    turns = directions[self.direction]['turns']
                    left_turn = turns[0]  # Assuming the first turn in the list is left
                    self.move_plan = [self.direction, left_turn, left_turn]
                elif action == 'right':
                    turns = directions[self.direction]['turns']
                    right_turn = turns[-1]  # Assuming the last turn in the list is right
                    self.move_plan = [self.direction, self.direction, right_turn, self.direction, self.direction]

    def move(self, grid):
        if not self.move_plan:
            self.plan_moves(grid)

        if self.move_plan:
            move_direction = self.move_plan.pop(0)
            self.direction = move_direction
            row, col = self.position
            d_row, d_col = directions[move_direction]['move']
            n_rows, n_cols = grid.shape
            next_row = (row + d_row) % n_rows
            next_col = (col + d_col) % n_cols

            if grid[next_row, next_col] in (1, 2):
                self.position = (next_row, next_col)

# Directions with associated potential turning directions at intersections
directions = {
    'N': {'move': (-1, 0), 'turns': ['W', 'S']},
    'S': {'move': (1, 0), 'turns': ['E', 'N']},
    'E': {'move': (0, 1), 'turns': ['N', 'W']},
    'W': {'move': (0, -1), 'turns': ['S', 'E']}
}

def create_grid(n_rows, n_cols):
    grid = np.zeros((n_rows, n_cols))
    for i in range(n_rows):
        if i % 15 == 0 or i % 15 == 1 or i >= n_rows - 2:
            grid[i, :] = 1
    for j in range(n_cols):
        if j % 20 == 0 or j % 20 == 1 or j >= n_cols - 2:
            grid[:, j] = 1
    for i in range(n_rows):
        for j in range(n_cols):
            if grid[i, j] == 1 and ((i % 15 <= 1 or i >= n_rows - 2) and (j % 20 <= 1 or j >= n_cols - 2)):
                grid[i, j] = 2
    return grid

def initialise_cars(grid, num_cars=10):
    cars = []
    while len(cars) < num_cars:
        row, col = np.random.randint(grid.shape[0]), np.random.randint(grid.shape[1])
        if grid[row, col] in (1, 2):
            direction = np.random.choice(list(directions.keys()))
            cars.append(Car((row, col), direction))
    return cars

def observe(cars, grid):
    plt.imshow(grid, cmap='binary', alpha=0.8)
    for car in cars:
        plt.scatter(car.position[1], car.position[0], color='red', s=40)

def animate(frame_num, cars, grid):
    for car in cars:
        car.move(grid)
    plt.cla()
    observe(cars, grid)

n_rows, n_cols = 60, 60
grid = create_grid(n_rows, n_cols)
cars = initialise_cars(grid, 10)

fig, ax = plt.subplots()
ani = FuncAnimation(fig, animate, fargs=(cars, grid), frames=100, interval=1)
plt.show()
