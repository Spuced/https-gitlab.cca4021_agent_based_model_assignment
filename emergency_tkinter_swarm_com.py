import tkinter as tk
import random
from collections import deque
import numpy as np
import math
from create_office import layout

# Simulation Properties
open_space = 0
wall = 1
exit = 2
grid_size = 100
cell_size = 8  # Adjust the size of each cell
center_of_mass_radius = 2  # Radius to consider for calculating local center of mass

grid = layout()

class Follower:
    def __init__(self):
        self.x = random.randint(1, grid_size - 2)
        self.y = random.randint(1, grid_size - 2)
        self.stuck_counter = 0
        self.random_movement_counter = 0
        self.random_movement_duration = 50
        self.escaped = False

    def follow_local_center_of_mass(self, leaders, followers):
        if self.move_towards_exit():
            self.escaped = True
            return True
        elif self.random_movement_counter > 0:
            self.random_movement_counter -= 1
            self.random_movement()
        else:
            center_x, center_y = self.calculate_local_center_of_mass(leaders, followers)
            move_x = np.sign(center_x - self.x)
            move_y = np.sign(center_y - self.y)
            new_x = int(self.x + move_x)
            new_y = int(self.y + move_y)
            if 0 <= new_x < grid_size and 0 <= new_y < grid_size:
                if grid[new_x][new_y] == exit:
                    self.escaped = True
                    return True
                elif grid[new_x][new_y] == open_space:
                    self.x = new_x
                    self.y = new_y
                    if move_x == 0 and move_y == 0:
                        self.stuck_counter += 1
                        if self.stuck_counter >= 10:
                            self.random_movement_counter = self.random_movement_duration
                            self.stuck_counter = 0
                    else:
                        self.stuck_counter = 0
                elif grid[new_x][new_y] == wall:  # Check if there's a wall
                    self.random_movement_counter = self.random_movement_duration
                    self.stuck_counter = 0
            else:
                self.random_movement_counter = self.random_movement_duration
                self.stuck_counter = 0

        return False

    def calculate_local_center_of_mass(self, leaders, followers):
        total_mass = 1  # Initialize with own position
        center_x = self.x
        center_y = self.y

        for leader in leaders:
            if abs(leader.x - self.x) <= center_of_mass_radius and abs(leader.y - self.y) <= center_of_mass_radius:
                total_mass += 1
                center_x += leader.x
                center_y += leader.y

        for follower in followers:
            if abs(follower.x - self.x) <= center_of_mass_radius and abs(follower.y - self.y) <= center_of_mass_radius:
                total_mass += 1
                center_x += follower.x
                center_y += follower.y

        if total_mass > 1:  # Avoid division by zero
            return center_x / total_mass, center_y / total_mass
        else:
            return self.x, self.y

    def random_movement(self):
        dx, dy = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_x < grid_size and 0 <= new_y < grid_size and grid[new_x][new_y] == open_space:
            self.x = new_x
            self.y = new_y

    def find_exit(self):
        for i in range(self.x - 10, self.x + 11):
            for j in range(self.y - 10, self.y + 11):
                if 0 <= i < grid_size and 0 <= j < grid_size and grid[i][j] == exit:
                    return i, j
        return None

    def move_towards_exit(self):
        exit_pos = self.find_exit()
        if exit_pos:
            move_x = np.sign(exit_pos[0] - self.x)
            move_y = np.sign(exit_pos[1] - self.y)
            new_x = int(self.x + move_x)
            new_y = int(self.y + move_y)
            if grid[new_x][new_y] == exit:
                self.escaped = True
                return True
            elif 0 <= new_x < grid_size and 0 <= new_y < grid_size and grid[new_x][new_y] == open_space:
                self.x = new_x
                self.y = new_y
        return False

class FireWarden:
    def __init__(self):
        self.x = random.randint(1, grid_size - 2)
        self.y = random.randint(1, grid_size - 2)
        self.path_to_exit = None  # Initialize path_to_exit attribute
        self.escaped = False

    def move(self):
        if not self.path_to_exit:
            self.path_to_exit = self.find_path_to_exit()

        if self.path_to_exit:
            self.x, self.y = self.path_to_exit.pop(0)
            if grid[self.x][self.y] == exit:
                self.escaped = True
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
    global followers
    global fire_wardens
    followers = [Follower() for _ in range(100)]
    fire_wardens = [FireWarden() for _ in range(200)]

def update():
    global fire_wardens, followers
    updated_fire_wardens = []
    for fire_warden in fire_wardens:
        if not fire_warden.move():
            updated_fire_wardens.append(fire_warden)
    fire_wardens = updated_fire_wardens

    updated_followers = []
    for follower in followers:
        if not follower.follow_local_center_of_mass(fire_wardens, followers):
            if grid[follower.x][follower.y] == exit:
                continue
            updated_followers.append(follower)
    followers = updated_followers

def draw_grid(canvas):
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i][j] == wall:
                canvas.create_rectangle(j * cell_size, i * cell_size, (j + 1) * cell_size, (i + 1) * cell_size, fill='black')
            elif grid[i][j] == exit:
                canvas.create_rectangle(j * cell_size, i * cell_size, (j + 1) * cell_size, (i + 1) * cell_size, fill='green')
    for follower in followers:
        canvas.create_oval(follower.y * cell_size, follower.x * cell_size, (follower.y + 1) * cell_size, (follower.x + 1) * cell_size, fill='red')
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
