import tkinter as tk
import random
from collections import deque
from create_office import layout
import math
import numpy as np

# Simulation Properties
open_space, wall, exit, fire = 0, 1, 2, 3
grid_size = 100
cell_size = 8  # Size of each cell in pixels
cell_size = 8  # Adjust the size of each cell
center_of_mass_radius = 10

grid = layout()


exits = []
for i in range(grid_size):
    for j in range(grid_size):
        if grid[i][j] == exit:
            exits.append([i, j])

class Workers:

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
        self.panic = 1 if random.random() < 0.4 else 0  # Initial panic state

    def worker_update(self):
        global escaped_workers, occupied_positions

        # Do nothing if they die
        if self.die():
            return True
        
        steps_to_check = 10  # Check the next n steps for fire
        if not self.path_to_exit or self.is_path_blocked(self.path_to_exit, steps_to_check):
            self.path_to_exit = self.find_path_to_exit()

        # Make them calm if they see the exit
        if self.should_change_panic():
            self.panic = 1 - self.panic  # Change panic state

        # Check distance to exit and change panic state accordingly
        if self.distance_to_exit() <= 5:
            self.panic = 0  # Set panic state to calm if exit is within 5 units

        # They shold move randomly if panicked
        if self.panic:
            self.swarm(workers)

        # If calm move along the path to the exit
        else:
            if self.path_to_exit:
                next_x, next_y = self.path_to_exit[0]  # Peek the next position without removing it

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
        return False
    
    def calculate_local_center_of_mass(self, workers):
        total_mass = 1  # Initialize with own position
        center_x = self.x
        center_y = self.y

        for worker in workers:
            if abs(worker.x - self.x) <= center_of_mass_radius and abs(worker.y - self.y) <= center_of_mass_radius:
                total_mass += 1
                center_x += worker.x
                center_y += worker.y

        if total_mass > 1:  # Avoid division by zero
            return center_x / total_mass, center_y / total_mass
        else:
            return self.x, self.y

    def should_change_panic(self):
        nearby_agents = self.get_nearby_agents()
        num_panicked = sum(agent.panic for agent in nearby_agents)
        num_calm = len(nearby_agents) - num_panicked
        return num_panicked < num_calm if self.panic else num_calm < num_panicked

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

    def swarm(self, workers):
            center_x, center_y = self.calculate_local_center_of_mass(workers)
            move_x = np.sign(center_x - self.x)
            move_y = np.sign(center_y - self.y)
            new_x = int(self.x + move_x)
            new_y = int(self.y + move_y)
            if 0 <= new_x < grid_size and 0 <= new_y < grid_size and grid[new_x][new_y] == open_space and (new_x, new_y) not in occupied_positions:
                occupied_positions.remove((self.x, self.y))
                self.x = new_x
                self.y = new_y
                occupied_positions.add((self.x, self.y))

    # Check up to n steps in the path for fire
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
                nx, ny = x + dx, y + dy
                if 0 <= nx < grid_size and 0 <= ny < grid_size and not visited[nx][ny]:
                    if grid[nx][ny] == exit:
                        return path + [(nx, ny)]
                    elif grid[nx][ny] == open_space:
                        queue.append((nx, ny, path + [(nx, ny)]))
                        visited[nx][ny] = True
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
    global workers, fires, escaped_workers, dead_workers, occupied_positions

    occupied_positions = set() 
    workers = [Workers() for _ in range(400)]
    fires = [Fire() for _ in range(1)]

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
    update()
    canvas.delete("all")
    draw_grid(canvas)
    worker_label.config(text="Workers Escaped: " + str(escaped_workers))
    dead_label.config(text="Workers Died: " + str(dead_workers))
    canvas.after(50, animate)  # Adjust the animation speed by changing the delay time

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

# Start animation
animate()

root.mainloop()