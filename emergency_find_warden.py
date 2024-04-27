import tkinter as tk
import random
from collections import deque
import csv
from create_office import layout

# Simulation Properties
open_space = 0
wall = 1
exit = 2
grid_size = 100
cell_size = 8  # Adjust the size of each cell
vision = 5

grid = layout()

# Creating classes for each agent type
class Panicker:
    def __init__(self):
        while True:
            self.x = random.randint(1, grid_size - 2)
            self.y = random.randint(1, grid_size - 2)
            if grid[self.x][self.y] == open_space:
                break

    def move(self):
        global fire_wardens, escaped_panickers
        
        # Check for exits within distance 10
        exits_within_range = []
        for i in range(grid_size):
            for j in range(grid_size):
                if grid[i][j] == exit:
                    distance = abs(j - self.y) + abs(i - self.x)
                    if distance <= 10:
                        exits_within_range.append((i, j))

        if exits_within_range:  # Move towards the closest exit
            min_distance = float('inf')
            closest_exit = None
            for exit_x, exit_y in exits_within_range:
                distance = abs(exit_x - self.x) + abs(exit_y - self.y)
                if distance < min_distance:
                    min_distance = distance
                    closest_exit = (exit_x, exit_y)
            if closest_exit:
                exit_x, exit_y = closest_exit
                dx = 1 if exit_y > self.y else -1
                dy = 1 if exit_x > self.x else -1
                clear_path = True
                for k in range(1, min_distance):
                    new_x = self.x + k * dx
                    new_y = self.y + k * dy
                    if not (0 <= new_x < grid_size and 0 <= new_y < grid_size) or grid[new_x][new_y] == wall:
                        clear_path = False
                        break
                if clear_path:
                    self.x, self.y = exit_x, exit_y
                    if grid[exit_x][exit_y] == exit:
                        escaped_panickers += 1
                        return True
                    return False  # Moved towards the exit but not escaped yet
        
        # Check for fire wardens within distance 10
        wardens_within_range = []
        for fire_warden in fire_wardens:
            distance = abs(fire_warden.x - self.x) + abs(fire_warden.y - self.y)
            if distance <= 10:
                wardens_within_range.append((fire_warden.x, fire_warden.y))

        if wardens_within_range:  # Move towards the closest warden
            min_distance = float('inf')
            closest_warden = None
            for warden_x, warden_y in wardens_within_range:
                distance = abs(warden_x - self.x) + abs(warden_y - self.y)
                if distance < min_distance:
                    min_distance = distance
                    closest_warden = (warden_x, warden_y)
            if closest_warden:
                warden_x, warden_y = closest_warden
                dx = 1 if warden_y > self.y else -1
                dy = 1 if warden_x > self.x else -1
                clear_path = True
                for k in range(1, min_distance):
                    new_x = self.x + k * dx
                    new_y = self.y + k * dy
                    if not (0 <= new_x < grid_size and 0 <= new_y < grid_size) or grid[new_x][new_y] == wall:
                        clear_path = False
                        break
                if clear_path:
                    self.x, self.y = warden_x, warden_y
                    return False  # Moved towards the warden
        
        # Move randomly
        potential_moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        random.shuffle(potential_moves)
        for move_x, move_y in potential_moves:
            new_x, new_y = self.x + move_x, self.y + move_y
            if 0 <= new_x < grid_size and 0 <= new_y < grid_size:
                if grid[new_x][new_y] == exit:
                    escaped_panickers += 1
                    return True
                elif grid[new_x][new_y] == open_space:
                    self.x, self.y = new_x, new_y
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
        global escaped_wardens
        if not self.path_to_exit:
            self.path_to_exit = self.find_path_to_exit()

        if self.path_to_exit:
            self.x, self.y = self.path_to_exit.pop(0)
            if grid[self.x][self.y] == exit:
                escaped_wardens += 1
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
    global panickers, fire_wardens, escaped_panickers, escaped_wardens
    panickers = [Panicker() for _ in range(200)]
    fire_wardens = [FireWarden() for _ in range(20)]
    escaped_panickers = 0
    escaped_wardens = 0

def update():
    global panickers, fire_wardens
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
    panicker_label.config(text="Panickers Escaped: " + str(escaped_panickers))
    warden_label.config(text="Wardens Escaped: " + str(escaped_wardens))
    csv_data.append([escaped_panickers, escaped_wardens])
    canvas.after(50, animate)  # Adjust the animation speed by changing the delay time


# Tkinter setup
initialise()
root = tk.Tk()
root.title("Panic Simulation")
canvas = tk.Canvas(root, width=grid_size * cell_size, height=grid_size * cell_size)
canvas.pack()

# Add labels to display the number of escaped panickers and fire wardens
panicker_label = tk.Label(root, text="Panickers Escaped: 0")
panicker_label.pack()
warden_label = tk.Label(root, text="Wardens Escaped: 0")
warden_label.pack()

csv_data = [["Panickers Escaped", "Wardens Escaped"]]
# Start animation
animate()

root.mainloop()

# Write the CSV data to a file
with open("escape_data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(csv_data)
