import tkinter as tk
import random
from collections import deque
import math
from create_office import layout

grid = layout()

# Simulation Properties
open_space, wall, exit, fire = 0, 1, 2, 3
grid_size = 100
cell_size = 8  # Size of each cell in pixels
number_of_workers = 500
number_of_fires = 1

# Mark the exits
exits = []
for i in range(grid_size):
    for j in range(grid_size):
        if grid[i][j] == exit:
            exits.append([i, j])

# Tkinter setup
root = tk.Tk()
root.title("Panic Simulation")
canvas = tk.Canvas(root, width=grid_size * cell_size, height=grid_size * cell_size)
canvas.pack()

# Input fields for parameters
panic_percent_input = tk.Entry(root)
panic_percent_input.insert(tk.END, str(0.4))
panic_percent_input.pack()

number_of_workers_input = tk.Entry(root)
number_of_workers_input.insert(tk.END, str(500))
number_of_workers_input.pack()

number_of_fires_input = tk.Entry(root)
number_of_fires_input.insert(tk.END, str(1))
number_of_fires_input.pack()

fire_spread_rate_input = tk.Entry(root)
fire_spread_rate_input.insert(tk.END, str(0.4))
fire_spread_rate_input.pack()

vision_input = tk.Entry(root)
vision_input.insert(tk.END, str(10))
vision_input.pack()

worker_label = tk.Label(root, text="Workers Escaped: 0")
worker_label.pack()

dead_label = tk.Label(root, text="Workers Died: 0")
dead_label.pack()

# Simulation functions
def start_simulation():
    global panic_percent, number_of_workers, number_of_fires, fire_spread_rate, vision
    panic_percent = float(panic_percent_input.get())
    number_of_workers = int(number_of_workers_input.get())
    number_of_fires = int(number_of_fires_input.get())
    fire_spread_rate = float(fire_spread_rate_input.get())
    vision = int(vision_input.get())
    initialise()
    run_step()

step_count = 0

def run_continuous():
    global step_count
    update()
    canvas.delete("all")
    draw_grid(canvas)
    worker_label.config(text="Workers Escaped: " + str(escaped_workers))
    dead_label.config(text="Workers Died: " + str(dead_workers))
    step_count += 1
    step_label.config(text="Step: " + str(step_count))
    if workers:
        root.after(50, run_continuous)

def run_step():
    global step_count
    update()
    canvas.delete("all")
    draw_grid(canvas)
    worker_label.config(text="Workers Escaped: " + str(escaped_workers))
    dead_label.config(text="Workers Died: " + str(dead_workers))
    step_count += 1
    step_label.config(text="Step: " + str(step_count))

def initialise():
    global workers, fires, escaped_workers, dead_workers, occupied_positions
    occupied_positions = set()
    workers = [Worker() for _ in range(number_of_workers)]
    fires = [Fire() for _ in range(number_of_fires)]
    escaped_workers = 0
    dead_workers = 0

def update():
    global workers, fires
    workers[:] = [worker for worker in workers if not worker.worker_update()]
    new_fires = []
    for fire in fires:
        new_fires.extend(fire.spread())
    fires.extend(Fire() for _ in range(len(new_fires)))
    fires[:] = [fire for fire in fires if (fire.x, fire.y) not in [(fx, fy) for fx, fy in new_fires]]

def draw_grid():
    canvas.delete("all")
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i][j] == wall:
                canvas.create_rectangle(j * cell_size, i * cell_size, (j + 1) * cell_size, (i + 1) * cell_size, fill='black')
            elif grid[i][j] == exit:
                canvas.create_rectangle(j * cell_size, i * cell_size, (j + 1) * cell_size, (i + 1) * cell_size, fill='green')
    for worker in workers:
        color = 'red' if worker.panic else 'green'
        canvas.create_oval(worker.y * cell_size, worker.x * cell_size, (worker.y + 1) * cell_size, (worker.x + 1) * cell_size, fill=color)
    for fire in fires:
        canvas.create_rectangle(fire.y * cell_size, fire.x * cell_size, (fire.y + 1) * cell_size, (fire.x + 1) * cell_size, fill='orange')

def animate():
    update()
    draw_grid()
    worker_label.config(text="Workers Escaped: " + str(escaped_workers))
    dead_label.config(text="Workers Died: " + str(dead_workers))
    root.after(50, animate)

# Simulation classes
class Worker:
    def __init__(self):
        self.panic_percent = 0.5
        self.vision = 10
        while True:
            self.x = random.randint(1, grid_size - 2)
            self.y = random.randint(1, grid_size - 2)
            if grid[self.x][self.y] == open_space and (self.x, self.y) not in occupied_positions:
                occupied_positions.add((self.x, self.y))
                break
        self.path_to_exit = None
        self.panic = 1 if random.random() <= self.panic_percent else 0
        self.stationary_time = 0

    def worker_update(self):
        global escaped_workers, occupied_positions, dead_workers
        initial_position = (self.x, self.y)
        if self.die():
            return True
        if self.should_change_panic():
            self.panic = 1 - self.panic
        if self.distance_to_exit() <= self.vision:
            self.panic = 0
        steps_to_check = self.vision
        patience = 10
        if self.panic != 1:
            if not self.path_to_exit or self.stationary_time > patience or self.is_path_blocked(self.path_to_exit, steps_to_check):
                self.path_to_exit = self.find_path_to_exit()
                self.stationary_time = 0
            if len(self.path_to_exit) == 0:
                self.panic = 1
        if self.panic:
            self.move_randomly()
        else:
            if self.path_to_exit:
                next_x, next_y = self.path_to_exit[0]
                if (next_x, next_y) not in occupied_positions:
                    self.path_to_exit.pop(0)
                    occupied_positions.remove((self.x, self.y))
                    self.x, self.y = next_x, next_y
                    occupied_positions.add((self.x, self.y))
                    if grid[self.x][self.y] == exit:
                        escaped_workers += 1
                        occupied_positions.remove((self.x, self.y))
                        return True
        if (self.x, self.y) == initial_position:
            self.stationary_time += 1
        else:
            self.stationary_time = 0
        return False

    def should_change_panic(self):
        nearby_agents = self.get_nearby_agents()
        num_panicked = sum(agent.panic for agent in nearby_agents)
        num_calm = len(nearby_agents) - num_panicked
        return num_panicked < num_calm if self.panic else num_calm < num_panicked

    def get_nearby_agents(self):
        nearby_agents = []
        for worker in workers:
            if worker != self and abs(worker.x - self.x) <= self.vision and abs(worker.y - self.y) <= self.vision:
                nearby_agents.append(worker)
        return nearby_agents

    def die(self):
        global dead_workers, occupied_positions
        if grid[self.x][self.y] == fire:
            occupied_positions.remove((self.x, self.y))
            dead_workers += 1
            return True

    def distance_to_exit(self):
        dists = [math.sqrt((exit_x - self.x)**2 + (exit_y - self.y)**2) for exit_x, exit_y in exits]
        min_dist = min(dists)
        return min_dist

    def move_randomly(self):
        possible_moves = [(self.x + dx, self.y + dy) for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]]
        random.shuffle(possible_moves)
        for new_x, new_y in possible_moves:
            if 0 <= new_x < grid_size and 0 <= new_y < grid_size and grid[new_x][new_y] == open_space and (new_x, new_y) not in occupied_positions:
                occupied_positions.remove((self.x, self.y))
                self.x, self.y = new_x, new_y
                occupied_positions.add((self.x, self.y))
                break

    def is_path_blocked(self, path, n):
        for x, y in path[:n]:
            if grid[x][y] == fire:
                return True
        return False

    def find_path_to_exit(self):
        visited = [[False for _ in range(grid_size)] for _ in range(grid_size)]
        queue = deque([(self.x, self.y, [])])
        visited[self.x][self.y] = True
        while queue:
            x, y, path = queue.popleft()
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < grid_size and 0 <= new_y < grid_size and not visited[new_x][new_y]:
                    if grid[new_x][new_y] == exit:
                        return path + [(new_x, new_y)]
                    elif grid[new_x][new_y] == open_space and (new_x, new_y) not in occupied_positions:
                        queue.append((new_x, new_y, path + [(new_x, new_y)]))
                        visited[new_x][new_y] = True
        return []

class Fire:
    def __init__(self, x=None, y=None):
        self.fire_x = random.randint(1, grid_size - 2)
        self.fire_y = random.randint(1, grid_size - 2)
        self.fire_spread_rate = 0.4
        if x is None or y is None:
            while True:
                self.x, self.y = self.fire_x, self.fire_y
                if grid[self.x][self.y] == open_space:
                    grid[self.x][self.y] = fire
                    break
        else:
            self.x, self.y = x, y
            grid[self.x][self.y] = fire

    def spread(self):
        spread_moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        open_adjacent_spaces = [
            (self.x + dx, self.y + dy) 
            for dx, dy in spread_moves 
            if 0 <= self.x + dx < grid_size and 0 <= self.y + dy < grid_size and grid[self.x + dx][self.y + dy] == open_space
        ]
        if open_adjacent_spaces and random.random() < self.fire_spread_rate:
            random.shuffle(open_adjacent_spaces)
            new_x, new_y = open_adjacent_spaces[0]
            grid[new_x][new_y] = fire
            return [(new_x, new_y)]
        return []

# Run simulation button

continuous_button = tk.Button(root, text="Run Continuous", command=run_continuous)
continuous_button.pack()

step_button = tk.Button(root, text="Step", command=run_step)
step_button.pack()

step_label = tk.Label(root, text="Step: 0")
step_label.pack()

start_button = tk.Button(root, text="Start Simulation", command=start_simulation)
start_button.pack()

root.mainloop()
