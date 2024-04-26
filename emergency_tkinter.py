import tkinter as tk
import random
from collections import deque

# Simulation Properties
open_space = 0
wall = 1
exit = 2
grid_size = 100
cell_size = 16  # Adjust the size of each cell

# Grid setup

# Set the outside wall
grid = [[wall if i == 0 or i == grid_size - 1 or j == 0 or j == grid_size - 1 else open_space for j in range(grid_size)] for i in range(grid_size)]

# Create the 4 office walls
for i in range(0, 46):
    for j in [45, 55]:
        grid[i][j] = wall
        grid[i][j] = wall
        grid[j][i] = wall
        grid[j][i] = wall

for i in range(55, 100):
    for j in [45, 55]:
        grid[i][j] = wall
        grid[i][j] = wall
        grid[j][i] = wall
        grid[j][i] = wall

# Create the internal doors
grid[45][24:26] = open_space, open_space
grid[55][24:26] = open_space, open_space
grid[45][75:77] = open_space, open_space
grid[55][75:77] = open_space, open_space

for row in range(24, 26):
    grid[row][45] = open_space
    grid[row][55] = open_space

for row in range(76, 78):
    grid[row][45] = open_space
    grid[row][55] = open_space

# Create the desks
for i in range(10, 35):
    for j in range(7, 38, 10):
        grid[i][j] = wall
        grid[i][j] = wall

    for j in range(63, 99, 10):
        grid[i][j] = wall
        grid[i][j] = wall

for i in range(65, 90):
    for j in range(7, 38, 10):
        grid[i][j] = wall
        grid[i][j] = wall

    for j in range(63, 99, 10):
        grid[i][j] = wall
        grid[i][j] = wall

# Set the exits
for i in range(49, 51):
    grid[0][i] = exit  # Top
    grid[99][i] = exit # Bottom
    grid[i][0] = exit  # Left
    grid[i][99] = exit  # Right

# Creating classes for each agent type
class Panicker:
    def __init__(self):
        while True:
            self.x = random.randint(1, grid_size - 2)
            self.y = random.randint(1, grid_size - 2)
            if grid[self.x][self.y] == open_space:
                break

    def move(self):
        potential_moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        random.shuffle(potential_moves)
        for move_x, move_y in potential_moves:
            new_x = self.x + move_x
            new_y = self.y + move_y
            if 0 <= new_x < grid_size and 0 <= new_y < grid_size:
                if grid[new_x][new_y] == exit:
                    return True
                elif grid[new_x][new_y] == open_space:
                    self.x = new_x
                    self.y = new_y
                    break
        return False
    
class FireWarden:
    def __init__(self):
        while True:
            self.x = random.randint(1, grid_size - 2)
            self.y = random.randint(1, grid_size - 2)
            if grid[self.x][self.y] == open_space:
                break
        self.path_to_exit = None  # Initialise path_to_exit attribute

    def move(self):
        if not self.path_to_exit:
            self.path_to_exit = self.find_path_to_exit()

        if self.path_to_exit:
            self.x, self.y = self.path_to_exit.pop(0)
            if grid[self.x][self.y] == exit:
                return True
        return False

    def find_path_to_exit(self):
        visited = [[False for _ in range(grid_size)] for _ in range(grid_size)]
        queue = deque([(self.x, self.y, [])])

        while queue:
            x, y, path = queue.popleft()
            if grid[x][y] == exit:
                return path

            visited[x][y] = True

            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < grid_size and 0 <= ny < grid_size and not visited[nx][ny] and grid[nx][ny] != wall:
                    queue.append((nx, ny, path + [(nx, ny)]))
                    visited[nx][ny] = True

        return []

def initialise():
    global panickers
    global fire_wardens
    panickers = [Panicker() for _ in range(100)]
    fire_wardens = [FireWarden() for _ in range(100)]

def update():
    global panickers
    global fire_wardens
    panickers = [panicker for panicker in panickers if not panicker.move()]
    fire_wardens = [fire_warden for fire_warden in fire_wardens if not fire_warden.move()]

def draw_grid(canvas):
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i][j] == wall:
                canvas.create_rectangle(j * cell_size, i * cell_size, (j + 1) * cell_size, (i + 1) * cell_size, fill='black')
            elif grid[i][j] == exit:
                canvas.create_rectangle(j * cell_size, i * cell_size, (j + 1) * cell_size, (i + 1) * cell_size, fill='green')
    for panicker in panickers:
        canvas.create_oval(panicker.y * cell_size, panicker.x * cell_size, (panicker.y + 1) * cell_size, (panicker.x + 1) * cell_size, fill='red')
    for fire_warden in fire_wardens:
        canvas.create_oval(fire_warden.y * cell_size, fire_warden.x * cell_size, (fire_warden.y + 1) * cell_size, (fire_warden.x + 1) * cell_size, fill='green')

def animate():
    update()
    canvas.delete("all")
    draw_grid(canvas)
    canvas.after(50, animate)  # Adjust the animation speed by changing the delay time

# Tkinter setup
initialise()
root = tk.Tk()
root.title("Panic Simulation")
canvas = tk.Canvas(root, width=grid_size * cell_size, height=grid_size * cell_size)
canvas.pack()

# Start animation
animate()

root.mainloop()
