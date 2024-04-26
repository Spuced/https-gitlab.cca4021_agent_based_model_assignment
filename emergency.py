import numpy as np
import matplotlib.pyplot as plt

# Create the floor plan
open_space = 0
wall = 1
exit = 2

# Create the grid
grid_size = 100
grid = np.zeros((grid_size, grid_size), dtype=int)

# Set the walls
grid[0, :] = wall
grid[:, 0] = wall
grid[99, :] = wall
grid[:, 99] = wall

# Set the exit
grid[0, 49:51] = exit


# Plot the office
plt.figure(figsize=(10, 10))
plt.imshow(grid, cmap='Greys')
plt.colorbar(label='Cell Type')

# Enhance the plot
plt.title('Office Floor Plan')
plt.axis('off')  # Turn off axis numbering
plt.show()

# Default Class
class panickers:
    def __init__(self, grid):
        
        # Randomly place a panicker in an open space
        placed = False
        while not placed:
            x = random.randint(1, grid_size - 2)
            y = random.randint(1, grid_size - 2)
            if grid[x, y] == open_space:
                self.x = x
                self.y = y
                placed = True