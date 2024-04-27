import tkinter as tk
import random
from collections import deque
from create_office import layout
import matplotlib.pyplot as plt

# Default Properties
open_space, wall, exit, fire = 0, 1, 2, 3
grid_size = 100

# A GUI for simulation parameters
app = tk.Tk()
app.title("Simulation Parameters (Close After Submitting)")

# Variables initialization with Tkinter
cell_size_var = tk.IntVar(value=8)
desks_var = tk.BooleanVar(value=True)
door_width_var = tk.IntVar(value=4)
exit_locations_var = tk.StringVar(value="top, bottom, left, right")
panic_percent_var = tk.DoubleVar(value=0.3)
panic_change_threshold_var = tk.DoubleVar(value=0.7)
force_calm_var = tk.BooleanVar(value=False)
steps_to_check_var = tk.IntVar(value=15)
patience_var = tk.IntVar(value=10)
num_workers_var = tk.IntVar(value=1000)
num_fires_var = tk.IntVar(value=1)
fire_x_var = tk.IntVar(value=random.randint(1, 98))
fire_y_var = tk.IntVar(value=random.randint(1, 98))
fire_spread_var = tk.DoubleVar(value=0.5)
random_seed_var = tk.IntVar(value=1234)

def submit():

    global cell_size, desks, door_width, exit_locations, panic_percent, panic_change_threshold, force_calm, steps_to_check, patience, num_workers, num_fires, fire_x, fire_y, fire_spread, random_seed

    # Convert the parameters to their normal types using get()
    cell_size = cell_size_var.get()
    desks = desks_var.get()
    door_width = door_width_var.get()
    exit_locations = exit_locations_var.get()
    panic_percent = panic_percent_var.get()
    panic_change_threshold = panic_change_threshold_var.get()
    force_calm = force_calm_var.get()
    steps_to_check = steps_to_check_var.get()
    patience = patience_var.get()
    num_workers = num_workers_var.get()
    num_fires = num_fires_var.get()
    fire_x = fire_x_var.get()
    fire_y = fire_y_var.get()
    fire_spread = fire_spread_var.get()
    random_seed = random_seed_var.get()

# GUI Layout for entering parameters
tk.Label(app, text="Cell Size").grid(row=0, column=0)
tk.Entry(app, textvariable=cell_size_var).grid(row=0, column=1)

tk.Label(app, text="Desks (True/False)").grid(row=1, column=0)
tk.Entry(app, textvariable=desks_var).grid(row=1, column=1)

tk.Label(app, text="Door Width").grid(row=2, column=0)
tk.Entry(app, textvariable=door_width_var).grid(row=2, column=1)

tk.Label(app, text="Exit Locations (comma separated)").grid(row=3, column=0)
tk.Entry(app, textvariable=exit_locations_var).grid(row=3, column=1)

tk.Label(app, text="Panic Percent").grid(row=4, column=0)
tk.Entry(app, textvariable=panic_percent_var).grid(row=4, column=1)

tk.Label(app, text="Panic Change Threshold").grid(row=5, column=0)
tk.Entry(app, textvariable=panic_change_threshold_var).grid(row=5, column=1)

tk.Label(app, text="Force Calm (True/False)").grid(row=6, column=0)
tk.Entry(app, textvariable=force_calm_var).grid(row=6, column=1)

tk.Label(app, text="Vision").grid(row=7, column=0)
tk.Entry(app, textvariable=steps_to_check_var).grid(row=7, column=1)

tk.Label(app, text="Patience").grid(row=8, column=0)
tk.Entry(app, textvariable=patience_var).grid(row=8, column=1)

tk.Label(app, text="Number of Workers").grid(row=9, column=0)
tk.Entry(app, textvariable=num_workers_var).grid(row=9, column=1)

tk.Label(app, text="Number of Fires").grid(row=10, column=0)
tk.Entry(app, textvariable=num_fires_var).grid(row=10, column=1)

tk.Label(app, text="Fire X Coordinate").grid(row=11, column=0)
tk.Entry(app, textvariable=fire_x_var).grid(row=11, column=1)

tk.Label(app, text="Fire Y Coordinate").grid(row=12, column=0)
tk.Entry(app, textvariable=fire_y_var).grid(row=13, column=1)

tk.Label(app, text="Fire Spread").grid(row=14, column=0)
tk.Entry(app, textvariable=fire_spread_var).grid(row=14, column=1)

tk.Label(app, text="Random Seed").grid(row=15, column=0)
tk.Entry(app, textvariable=random_seed_var).grid(row=15, column=1)

tk.Button(app, text="Submit", command=submit).grid(row=16, columnspan=2)

app.mainloop()

# Set the seed
random.seed(random_seed)

# Create the office layout
grid = layout(desks=desks, door_width=door_width, exit_locations=exit_locations)

# Mark the exits
exits = []
for i in range(grid_size):
    for j in range(grid_size):
        if grid[i][j] == exit:
            exits.append([i, j])

class Worker:

    # Place workers randomly in open space
    def __init__(self):
        while True:
            self.x = random.randint(1, grid_size - 2)
            self.y = random.randint(1, grid_size - 2)
            if grid[self.x][self.y] == open_space and (self.x, self.y) not in occupied_positions:
                occupied_positions.add((self.x, self.y))
                break

        # Initialise their path and panic state
        self.path_to_exit = None
        self.panic = 1 if random.random() <= panic_percent else 0  # Initial panic state
        self.stationary_time = 0 # The length of time they have been stationary

    def worker_update(self):
        global escaped_workers, occupied_positions

        initial_position = (self.x, self.y)

        # Check if they die
        if self.die():
            return True
        
        # Make them take on the panic state of their neighbours
        if self.should_change_panic():
            self.panic = 1 - self.panic  # Change panic state

        # Check distance to exit and change panic state accordingly
        if self.distance_to_exit() <= 5:
            self.panic = 0  # Set panic state to calm if exit is within 5 units
        
        # If fire blocks the next n steps
        # Or if they have been stationary for n inerations they should calulate a new path
        if self.panic != 1:
            if not self.path_to_exit or self.stationary_time > patience or self.is_path_blocked(self.path_to_exit, steps_to_check):
                self.path_to_exit = self.find_path_to_exit()
                self.stationary_time = 0

            # Make them panicked if there is no escape route
            if len(self.path_to_exit) == 0:
                self.panic = 1

        # For comparison see how they perform when always calm
        if force_calm:
            self.panic = 0

        # They shold move randomly if panicked
        if self.panic:
            self.move_randomly()

        # If calm move along the path to the exit
        else:
            if self.path_to_exit:
                next_x, next_y = self.path_to_exit[0]  # Check the next position

                # If it is free move them along their path
                if (next_x, next_y) not in occupied_positions:
                    self.path_to_exit.pop(0)  # Remove the position as we are about to move there
                    occupied_positions.remove((self.x, self.y))
                    self.x, self.y = next_x, next_y
                    occupied_positions.add((self.x, self.y))

                    # If they reach an exit they can be removed
                    if grid[self.x][self.y] == exit:
                        escaped_workers += 1
                        occupied_positions.remove((self.x, self.y))
                        return True
                    
        # Check if the worker has moved
        if (self.x, self.y) == initial_position:
            self.stationary_time += 1  # Increment stationary time if position has not changed
        else:
            self.stationary_time = 0  # Reset stationary time if the worker has moved

        return False
    
    # Change their panic level based on their neighbours
    def should_change_panic(self):
        nearby_agents = self.get_nearby_agents()
        if not nearby_agents:
            return False  # No change if no nearby agents

        num_panicked = sum(agent.panic for agent in nearby_agents)
        num_nearby = len(nearby_agents)
        panic_ratio = num_panicked / num_nearby

        # Change staes based on the threshold
        if self.panic and panic_ratio <= (1 - panic_change_threshold):
            return True  # Change from panic to calm if less than (1 - threshold) are panicked
        elif not self.panic and panic_ratio > panic_change_threshold:
            return True  # Change from calm to panic if more than threshold are panicked

        return False

    def get_nearby_agents(self):
        nearby_agents = []
        for worker in workers:
            if worker != self and abs(worker.x - self.x) <= 5 and abs(worker.y - self.y) <= 5:
                nearby_agents.append(worker)
        return nearby_agents
    
    # They die if they touch fire
    def die(self):

        global dead_workers, occupied_positions
        if grid[self.x][self.y] == fire:
            occupied_positions.remove((self.x, self.y))
            dead_workers += 1
            return True

    def distance_to_exit(self):
        dists = [abs(exit_x - self.x) + abs(exit_y - self.y) for exit_x, exit_y in exits]
        min_dist = min(dists)
        return min_dist
        
    # Move Panicked agents randomly
    def move_randomly(self):
        possible_moves = [(self.x + dx, self.y + dy) for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]]
        random.shuffle(possible_moves)
        for new_x, new_y in possible_moves:
            if 0 <= new_x < grid_size and 0 <= new_y < grid_size and grid[new_x][new_y] == open_space and (new_x, new_y) not in occupied_positions:
                occupied_positions.remove((self.x, self.y))
                self.x, self.y = new_x, new_y
                occupied_positions.add((self.x, self.y))
                break

    # Check up to n steps in the path for fire
    def is_path_blocked(self, path, n):
        for x, y in path[:n]:
            if grid[x][y] == fire:
                return True
        return False
    
    # Find the shortest path to an exit for each agent
    def find_path_to_exit(self):

        # Create list to keep track of visited cells.
        visited = [[False for _ in range(grid_size)] for _ in range(grid_size)]
        # Start the queue with the initial position of this worker and an empty path.
        queue = deque([(self.x, self.y, [])])
        visited[self.x][self.y] = True

        # Continue searching until there are no more cells to explore.
        while queue:
            x, y, path = queue.popleft()

            # Explore all adjacent cells (up, down, left, right).
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                new_x, new_y = x + dx, y + dy
                # Ensure the new position is within the grid bounds.
                if 0 <= new_x < grid_size and 0 <= new_y < grid_size and not visited[new_x][new_y]:
                    # Check if the adjacent cell is an exit.
                    if grid[new_x][new_y] == exit:
                        # Return the path to this exit, appending the exit position to the current path.
                        return path + [(new_x, new_y)]
                    
                    # If the adjacent cell is open space, it's a valid cell to move to.
                    #elif grid[nx][ny] == open_space:
                    elif grid[new_x][new_y] == open_space and (new_x, new_y) not in occupied_positions:

                        # Enqueue this cell along with the updated path.
                        queue.append((new_x, new_y, path + [(new_x, new_y)]))

                        # Mark this cell as visited to avoid revisiting.
                        visited[new_x][new_y] = True

        # If no path to an exit was found, return an empty list.
        return []

class Fire:

    # Create a fire randomly in the grid
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

    # The fire spreads randomly into an adjacent tile
    def spread(self):
        spread_moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        # Only spread into adjacent spaces
        open_adjacent_spaces = [
            (self.x + dx, self.y + dy) 
            for dx, dy in spread_moves 
            if 0 <= self.x + dx < grid_size and 0 <= self.y + dy < grid_size and grid[self.x + dx][self.y + dy] == open_space
        ]

        if open_adjacent_spaces and random.random() < fire_spread:  # Check if there are open spaces and if fire spreads
            random.shuffle(open_adjacent_spaces)
            new_x, new_y = open_adjacent_spaces[0]  # Spread to the first shuffled open space
            grid[new_x][new_y] = fire
            return [(new_x, new_y)]
        return []

# Create the two agent types
def initialise():
    global workers, fires, escaped_workers, dead_workers, occupied_positions, escaped_data, panic_data, deaths_data, fire_data

    occupied_positions = set() 
    workers = [Worker() for _ in range(num_workers)]
    fires = [Fire() for _ in range(num_fires)]

    escaped_workers = 0
    dead_workers = 0

    escaped_data = []
    panic_data = []
    deaths_data = []
    fire_data = []

# Update the two agent types
def update():
    global workers, fires, escaped_data, panic_data, deaths_data, fire_data
    workers = [worker for worker in workers if not worker.worker_update()]

    new_fires = []
    for fire in fires:
        new_fires.extend(fire.spread())
    for new_x, new_y in new_fires:
        fires.append(Fire(new_x, new_y))

    # Record data for plotting
    escaped_data.append(escaped_workers)
    panic_data.append(sum(worker.panic for worker in workers))
    deaths_data.append(dead_workers)
    fire_data.append(len(fires))

def draw_grid(canvas):
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
    canvas.delete("all")
    draw_grid(canvas)
    worker_label.config(text="Workers Escaped: " + str(escaped_workers))
    dead_label.config(text="Workers Died: " + str(dead_workers))
    canvas.after(50, animate)  # Adjust the animation speed by changing the delay time

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

# Tkinter setup
initialise()
root = tk.Tk()
root.title("Panic Simulation")
canvas = tk.Canvas(root, width=grid_size * cell_size, height=grid_size * cell_size)
canvas.pack()

worker_label = tk.Label(root, text="Workers Escaped: 0")
worker_label.pack()

dead_label = tk.Label(root, text="Workers Died: 0")
dead_label.pack()

continuous_button = tk.Button(root, text="Run Continuous", command=run_continuous)
continuous_button.pack()

step_button = tk.Button(root, text="Step", command=run_step)
step_button.pack()

step_label = tk.Label(root, text="Step: 0")
step_label.pack()

root.mainloop()

# Plot the results
plt.plot(escaped_data, label='Escaped Workers')
plt.plot(panic_data, label='Panic Level')
plt.plot(deaths_data, label='Dead Workers')
#plt.plot(fire_data, label='Fire Spread')
plt.xlabel('Time Step')
plt.ylabel('Values')
plt.title('Simulation Results')
plt.legend()
plt.show()