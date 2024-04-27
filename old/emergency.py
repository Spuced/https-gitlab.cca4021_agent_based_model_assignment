import numpy as np
import matplotlib.pyplot as plt
import random
from matplotlib.animation import FuncAnimation

# Grid Setup
open_space = 0
wall = 1
exit = 2
grid_size = 100
grid = np.zeros((grid_size, grid_size), dtype=int)
grid[0, :] = wall
grid[:, 0] = wall
grid[-1, :] = wall
grid[:, -1] = wall
grid[0, 49:51] = exit

class Panickers:
    def __init__(self):
        placed = False
        while not placed:
            x = random.randint(1, grid_size - 2)
            y = random.randint(1, grid_size - 2)
            if grid[x, y] == open_space:
                self.x = x
                self.y = y
                placed = True

    def move(self):
        potential_moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        random.shuffle(potential_moves)  # Shuffle potential moves
        for move_x, move_y in potential_moves:
            new_x = self.x + move_x
            new_y = self.y + move_y
            if 0 <= new_x < grid_size and 0 <= new_y < grid_size:
                if grid[new_x, new_y] == exit:
                    return True  # Indicate this panicker should be removed
                elif grid[new_x, new_y] == open_space:
                    grid[self.x, self.y] = open_space  # Reset previous position
                    self.x = new_x
                    self.y = new_y
                    grid[self.x, self.y] = 3  # Set new position
                    break  # Exit the loop once a valid move is made
        return False

def initialise():
    global panickers_list
    panickers_list = [Panickers() for _ in range(100)]

def observe():
    global scatters
    for scatter in scatters:
        scatter.remove()
    scatters = []
    for panicker in panickers_list:
        scatters.append(ax.scatter(panicker.y, panicker.x, color='red', s=80))

def update(frame):
    global panickers_list
    panickers_list = [panicker for panicker in panickers_list if not panicker.move()]  # Remove people that reach the exit

# Setup for animation
fig, ax = plt.subplots(figsize=(10, 10))
initialise()
im = ax.imshow(grid, cmap='Greys', vmin=0, vmax=2)
fig.colorbar(im, ax=ax, label='Cell Type', ticks=[open_space, wall, exit])

scatters = []
def animate(frame):
    update(frame)
    observe()

ani = FuncAnimation(fig, animate, frames=5000, interval=0.1, repeat=False)
plt.show()
