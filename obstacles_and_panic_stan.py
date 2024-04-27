import tkinter as tk
import random
from collections import deque
from create_office import layout
import math

# Simulation Properties
open_space, wall, exit, fire = 0, 1, 2, 3
grid_size = 100
cell_size = 8  # Size of each cell in pixels
panic_percent = 0.5
number_of_workers = 500
number_of_fires = 1
fire_x = random.randint(1, grid_size - 2)
fire_y = random.randint(1, grid_size - 2)
fire_spread_rate = 0.4
vision = 10


grid = layout()
#grid = layout(desks=False, door_width=1, exit_locations=['top', 'left'])

# Mark the exits
exits = []
for i in range(grid_size):
    for j in range(grid_size):
        if grid[i][j] == exit:
            exits.append([i, j])

class Worker:

    # Place them randomly in open space
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
        self.stationary_time = 0  # Time for which the worker has been stationary

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
        if self.distance_to_exit() <= vision:
            self.panic = 0  # Set panic state to calm if exit is within 5 units
        
        # If fire blocks the next n steps
        # Or if they have been stationary for n inerations they should calulate a new path
        steps_to_check = vision
        patience = 10

        if self.panic != 1:
            if not self.path_to_exit or self.stationary_time > patience or self.is_path_blocked(self.path_to_exit, steps_to_check):
                self.path_to_exit = self.find_path_to_exit()
                self.stationary_time = 0

            # Make them panicked if there is no escape route
            if len(self.path_to_exit) == 0:
                self.panic = 1

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

    def should_change_panic(self):
        nearby_agents = self.get_nearby_agents()
        num_panicked = sum(agent.panic for agent in nearby_agents)
        num_calm = len(nearby_agents) - num_panicked
        return num_panicked < num_calm if self.panic else num_calm < num_panicked

    def get_nearby_agents(self):
        nearby_agents = []
        for worker in workers:
            if worker != self and abs(worker.x - self.x) <= vision and abs(worker.y - self.y) <= vision:
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

    # Check up to n steps in the path for fire
    def is_path_blocked(self, path, n):
        for x, y in path[:n]:
            if grid[x][y] == fire:
                return True
        return False

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
                self.x, self.y = fire_x, fire_y
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

        if open_adjacent_spaces and random.random() < fire_spread_rate:  # Check if there are open spaces and if fire spreads
            random.shuffle(open_adjacent_spaces)
            new_x, new_y = open_adjacent_spaces[0]  # Spread to the first shuffled open space
            grid[new_x][new_y] = fire
            return [(new_x, new_y)]
        return []

def initialise():
    global workers, fires, escaped_workers, dead_workers, occupied_positions

    occupied_positions = set() 
    workers = [Worker() for _ in range(number_of_workers)]
    fires = [Fire() for _ in range(number_of_fires)]

    escaped_workers = 0
    dead_workers = 0

def update():
    global workers, fires
    workers = [worker for worker in workers if not worker.worker_update()]

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
    for worker in workers:
        color = 'red' if worker.panic else 'green'
        canvas.create_oval(worker.y * cell_size, worker.x * cell_size, (worker.y + 1) * cell_size, (worker.x + 1) * cell_size, fill=color)
    for fire in fires:
        canvas.create_rectangle(fire.y * cell_size, fire.x * cell_size, (fire.y + 1) * cell_size, (fire.x + 1) * cell_size, fill='orange')

def animate():
    update()  # Assumes this function updates the positions of workers and fire locations
    canvas.delete("dynamic")  # Delete only dynamic objects
    draw_grid(canvas)
    worker_label.config(text="Workers Escaped: " + str(escaped_workers))
    dead_label.config(text="Workers Died: " + str(dead_workers))
    canvas.after(50, animate)  # Adjust the animation speed by changing the delay time

step_count = 0

def run_continuous():
    global step_count, panic_percent, number_of_workers, number_of_fires, fire_spread_rate, vision
    # Retrieve parameter values from input fields
    panic_percent = float(panic_percent_input.get())
    number_of_workers = int(number_of_workers_input.get())
    number_of_fires = int(number_of_fires_input.get())
    fire_spread_rate = float(fire_spread_rate_input.get())
    vision = int(vision_input.get())

    step_count = 0
    initialise()  # Reinitialize the simulation with new parameters
    update()
    canvas.delete("all")
    draw_grid(canvas)
    worker_label.config(text="Workers Escaped: " + str(escaped_workers))
    dead_label.config(text="Workers Died: " + str(dead_workers))
    step_label.config(text="Step: " + str(step_count))
    if workers:
        root.after(50, run_continuous)

def run_step():
    global step_count, panic_percent, number_of_workers, number_of_fires, fire_spread_rate, vision
    # Retrieve parameter values from input fields
    panic_percent = float(panic_percent_input.get())
    number_of_workers = int(number_of_workers_input.get())
    number_of_fires = int(number_of_fires_input.get())
    fire_spread_rate = float(fire_spread_rate_input.get())
    vision = int(vision_input.get())

    step_count += 1
    update()
    canvas.delete("all")
    draw_grid(canvas)
    worker_label.config(text="Workers Escaped: " + str(escaped_workers))
    dead_label.config(text="Workers Died: " + str(dead_workers))
    step_label.config(text="Step: " + str(step_count))

# Tkinter setup
initialise()
root = tk.Tk()
root.title("Panic Simulation")
canvas = tk.Canvas(root, width=grid_size * cell_size, height=grid_size * cell_size)
canvas.pack()

# Input fields for parameters
panic_percent_input = tk.Entry(root)
panic_percent_input.insert(tk.END, str(panic_percent))
panic_percent_input.pack()

number_of_workers_input = tk.Entry(root)
number_of_workers_input.insert(tk.END, str(number_of_workers))
number_of_workers_input.pack()

number_of_fires_input = tk.Entry(root)
number_of_fires_input.insert(tk.END, str(number_of_fires))
number_of_fires_input.pack()

fire_spread_rate_input = tk.Entry(root)
fire_spread_rate_input.insert(tk.END, str(fire_spread_rate))
fire_spread_rate_input.pack()

vision_input = tk.Entry(root)
vision_input.insert(tk.END, str(vision))
vision_input.pack()

worker_label = tk.Label(root, text="Workers Escaped: 0")
worker_label.pack()

dead_label = tk.Label(root, text="Workers Died: 0")
dead_label.pack()

# Buttons to start the simulation
continuous_button = tk.Button(root, text="Run Continuous", command=run_continuous)
continuous_button.pack()

step_button = tk.Button(root, text="Step", command=run_step)
step_button.pack()

# Label to display current step
step_label = tk.Label(root, text="Step: 0")
step_label.pack()

root.mainloop()
