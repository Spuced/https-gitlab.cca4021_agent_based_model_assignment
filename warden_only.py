import tkinter as tk
import random
from collections import deque
from create_office import layout

# Simulation Properties
open_space, wall, exit, fire = 0, 1, 2, 3
grid_size = 100
cell_size = 8  # Size of each cell in pixels
cell_size = 8  # Adjust the size of each cell

grid = layout()

class FireWarden:
    def __init__(self):
        while True:
            self.x = random.randint(1, grid_size - 2)
            self.y = random.randint(1, grid_size - 2)
            if grid[self.x][self.y] == open_space:
                break
        self.path_to_exit = None

    def move(self):
        global escaped_wardens
        steps_to_check = 5  # Check the next 5 steps; adjust this value as needed
        if not self.path_to_exit or self.is_path_blocked(self.path_to_exit, steps_to_check):
            self.path_to_exit = self.find_path_to_exit()

        if self.path_to_exit:
            self.x, self.y = self.path_to_exit.pop(0)
            if grid[self.x][self.y] == exit:
                escaped_wardens += 1
                return True
        return False

    def is_path_blocked(self, path, n):
        # Check up to n steps in the path for obstacles
        for x, y in path[:n]:
            if grid[x][y] in (fire, wall):
                return True
        return False

    def find_path_to_exit(self):
        visited = [[False for _ in range(grid_size)] for _ in range(grid_size)]
        queue = deque([(self.x, self.y, [])])
        visited[self.x][self.y] = True

        while queue:
            x, y, path = queue.popleft()

            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < grid_size and 0 <= ny < grid_size and not visited[nx][ny]:
                    if grid[nx][ny] == exit:
                        return path + [(nx, ny)]
                    elif grid[nx][ny] == open_space:
                        queue.append((nx, ny, path + [(nx, ny)]))
                        visited[nx][ny] = True
        return []


class Fire:
    def __init__(self, x=None, y=None):
        if x is None or y is None:
            while True:
                self.x, self.y = random.randint(1, grid_size - 2), random.randint(1, grid_size - 2)
                if grid[self.x][self.y] == open_space:
                    grid[self.x][self.y] = fire
                    break
        else:
            self.x, self.y = x, y
            grid[self.x][self.y] = fire

    def spread(self):
        if random.random() < 0.6:
            spread_moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            random.shuffle(spread_moves)
            new_fires = set()
            for move_x, move_y in spread_moves:
                new_x, new_y = self.x + move_x, self.y + move_y
                if 0 <= new_x < grid_size and 0 <= new_y < grid_size and grid[new_x][new_y] == open_space:
                    new_fires.add((new_x, new_y))
                    break
            return list(new_fires)
        return []

def initialise():
    global panickers, fire_wardens, fires, escaped_wardens
    fire_wardens = [FireWarden() for _ in range(100)]
    fires = [Fire() for _ in range(1)]

    escaped_panickers = 0
    escaped_wardens = 0

def update():
    global fire_wardens, fires
    fire_wardens = [warden for warden in fire_wardens if not warden.move()]
    new_fires = []
    for fire in fires:
        new_fires.extend(fire.spread())
    for nx, ny in new_fires:
        fires.append(Fire(nx, ny))

def draw_grid(canvas):
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i][j] == wall:
                canvas.create_rectangle(j * cell_size, i * cell_size, (j + 1) * cell_size, (i + 1) * cell_size, fill='black')
            elif grid[i][j] == exit:
                canvas.create_rectangle(j * cell_size, i * cell_size, (j + 1) * cell_size, (i + 1) * cell_size, fill='green')

    for fire_warden in fire_wardens:
        canvas.create_oval(fire_warden.y * cell_size, fire_warden.x * cell_size, (fire_warden.y + 1) * cell_size, (fire_warden.x + 1) * cell_size, fill='green')
    for fire in fires:
        canvas.create_rectangle(fire.y * cell_size, fire.x * cell_size, (fire.y + 1) * cell_size, (fire.x + 1) * cell_size, fill='orange')

def animate():
    update()
    canvas.delete("all")
    draw_grid(canvas)
    warden_label.config(text="Wardens Escaped: " + str(escaped_wardens))
    canvas.after(50, animate)  # Adjust the animation speed by changing the delay time


# Tkinter setup
initialise()
root = tk.Tk()
root.title("Panic Simulation")
canvas = tk.Canvas(root, width=grid_size * cell_size, height=grid_size * cell_size)
canvas.pack()

warden_label = tk.Label(root, text="Wardens Escaped: 0")
warden_label.pack()

# Start animation
animate()

root.mainloop()