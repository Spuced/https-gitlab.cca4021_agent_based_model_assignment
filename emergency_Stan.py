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

def initialise():
    global panickers_list
    panickers_list = [Panickers() for _ in range(50)]

def observe():
    ax.clear()  # Clear only axes content
    im = ax.imshow(grid, cmap='Greys', vmin=0, vmax=2)
    ax.set_title('Office Floor Plan')
    ax.axis('off')
    
    for panicker in panickers_list:
        ax.scatter(panicker.y, panicker.x, color='red', s=80)

def update(frame):
    global panickers_list
    new_panickers_list = []

    for panicker in panickers_list:
        valid_move = False
        while not valid_move:
            move_x = random.randint(-1, 1)
            move_y = random.randint(-1, 1)
            new_x = panicker.x + move_x
            new_y = panicker.y + move_y

            if 0 <= new_x < grid_size and 0 <= new_y < grid_size:
                if grid[new_x, new_y] == open_space:
                    panicker.x = new_x
                    panicker.y = new_y
                    valid_move = True
                elif grid[new_x, new_y] == exit:
                    valid_move = True
                    continue

        if grid[panicker.x, panicker.y] != exit:
            new_panickers_list.append(panicker)

    panickers_list = new_panickers_list

# Setup for animation
fig, ax = plt.subplots(figsize=(10, 10))
initialise()
im = ax.imshow(grid, cmap='Greys', vmin=0, vmax=2)
fig.colorbar(im, ax=ax, label='Cell Type', ticks=[open_space, wall, exit])

def animate(frame):
    update(frame)
    observe()

ani = FuncAnimation(fig, animate, frames=50, interval=0.1, repeat=False)
plt.show()
