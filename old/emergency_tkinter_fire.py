import tkinter as tk
import random
from collections import deque
from create_office import layout

# Simulation Properties
open_space = 0
wall = 1
exit = 2
fire = 3
grid_size = 100
cell_size = 8  # Adjust the size of each cell

grid = layout()

class Panicker:
    def __init__(self):
        self.history = deque(maxlen=20)  # Store Most recent
        while True:
            self.x = random.randint(1, grid_size - 2)
            self.y = random.randint(1, grid_size - 2)
            if grid[self.x][self.y] == open_space:
                self.history.append((self.x, self.y))  # Add initial position to history
                break

    def move(self):
        global escaped_panickers
        potential_moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        random.shuffle(potential_moves)
        
        # First try to find a move that is not in history and is open space
        valid_moves = []
        fallback_moves = []
        for move_x, move_y in potential_moves:
            new_x = self.x + move_x
            new_y = self.y + move_y
            if 0 <= new_x < grid_size and 0 <= new_y < grid_size:
                if grid[new_x][new_y] == exit:
                    self.x = new_x
                    self.y = new_y
                    escaped_panickers += 1
                    return True  # Agent reaches an exit
                elif grid[new_x][new_y] == open_space:
                    if (new_x, new_y) not in self.history:
                        valid_moves.append((new_x, new_y))
                    else:
                        fallback_moves.append((new_x, new_y))
        
        # If there are valid moves not in history, execute one of them
        if valid_moves:
            new_x, new_y = random.choice(valid_moves)
            self.x = new_x
            self.y = new_y
            self.history.append((self.x, self.y))
            return False
        
        # If no valid moves and fallback is needed, pick one
        if fallback_moves:
            new_x, new_y = random.choice(fallback_moves)
            self.x = new_x
            self.y = new_y
            if len(self.history) == self.history.maxlen:
                self.history.popleft()  # Remove oldest entry if max length is reached
            self.history.append((self.x, self.y))
            return False

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
        if not self.path_to_exit or self.is_path_blocked(self.path_to_exit):
            self.path_to_exit = self.find_path_to_exit()

        if self.path_to_exit:
            self.x, self.y = self.path_to_exit.pop(0)
            if grid[self.x][self.y] == exit:
                escaped_wardens += 1
                return True  # The warden escapes
        return False  # The warden does not escape

    def is_path_blocked(self, path):
        for x, y in path:
            if grid[x][y] in (fire, wall):  # Assuming fire and wall are treated similarly as obstacles
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
                if 0 <= nx < grid_size and 0 <= ny < grid_size and not visited[nx][ny] and grid[nx][ny] != wall and grid[nx][ny] != fire:
                    queue.append((nx, ny, path + [(nx, ny)]))
                    visited[nx][ny] = True

        return []

class Fire:

    def __init__(self):
        while True:
            self.x = random.randint(1, grid_size - 2)
            self.y = random.randint(1, grid_size - 2)
            if grid[self.x][self.y] == open_space:
                grid[self.x][self.y] = fire  # Place fire on the grid
                break

    def place_at(self, x, y):
        self.x, self.y = x, y
        grid[self.x][self.y] = fire  # Place fire on the grid
        return self

    def spread(self):
        if random.random() < 1:  # Correcting the spread chance to 20%
            spread_moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            random.shuffle(spread_moves)
            new_fires = []  # Store new fire locations before updating the grid
            for move_x, move_y in spread_moves:
                new_x = self.x + move_x
                new_y = self.y + move_y
                if 0 <= new_x < grid_size and 0 <= new_y < grid_size:
                    if grid[new_x][new_y] == open_space:
                        new_fires.append((new_x, new_y))
                        break  # Only spread to one new cell at a time

            return new_fires
        return []  # No spread occurred

def initialise():
    global panickers, fire_wardens, fires, escaped_panickers, escaped_wardens
    panickers = [Panicker() for _ in range(100)]
    fire_wardens = [FireWarden() for _ in range(100)]
    fires = [Fire() for _ in range(1)]

    escaped_panickers = 0
    escaped_wardens = 0

def update():
    global panickers, fire_wardens, fires
    panickers = [panicker for panicker in panickers if not panicker.move()]
    fire_wardens = [fire_warden for fire_warden in fire_wardens if not fire_warden.move()]

    new_fires = []
    for fire in fires:
        new_fires.extend(fire.spread())
    for (nx, ny) in new_fires:
        fires.append(Fire().place_at(nx, ny))  # Add new fire instances based on spread locations

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
    for fire in fires:
        canvas.create_rectangle(fire.y * cell_size, fire.x * cell_size, (fire.y + 1) * cell_size, (fire.x + 1) * cell_size, fill='orange')

def animate():
    update()
    canvas.delete("all")
    draw_grid(canvas)
    panicker_label.config(text="Panickers Escaped: " + str(escaped_panickers))
    warden_label.config(text="Wardens Escaped: " + str(escaped_wardens))
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

# Start animation
animate()

root.mainloop()