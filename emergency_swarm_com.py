import tkinter as tk
import random
import numpy as np
from collections import deque

# Constants
open_space = 0
wall = 1
exit = 2
grid_size = 50
cell_size = 16  # Adjust the size of each cell
center_of_mass_radius = 10  # Radius to consider for calculating local center of mass

# Grid setup
grid = [[wall if i == 0 or i == grid_size - 1 or j == 0 or j == grid_size - 1 else open_space for j in range(grid_size)] for i in range(grid_size)]
grid[0][24:26] = [exit, exit]  # Define exit positions


class FireWarden:
    def __init__(self):
        self.x = random.randint(1, grid_size - 2)
        self.y = random.randint(1, grid_size - 2)
        self.path_to_exit = None  # Initialize path_to_exit attribute

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
    

class Follower:
    def __init__(self):
        self.x = random.randint(1, grid_size - 2)
        self.y = random.randint(1, grid_size - 2)

    def follow_local_center_of_mass(self, leaders, followers):
        center_x, center_y = self.calculate_local_center_of_mass(leaders, followers)
        move_x = np.sign(center_x - self.x)
        move_y = np.sign(center_y - self.y)
        new_x = int(self.x + move_x)
        new_y = int(self.y + move_y)
        if 0 <= new_x < grid_size and 0 <= new_y < grid_size:
            if grid[new_x][new_y] == exit:
                return True
            elif grid[new_x][new_y] == open_space:
                self.x = new_x
                self.y = new_y
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


def initialise():
    global leaders, followers
    leaders = [FireWarden() for _ in range(2)]
    followers = [Follower() for _ in range(50)]


def update():
    global leaders, followers
    updated_leaders = []
    for leader in leaders:
        if not leader.move():
            updated_leaders.append(leader)
    leaders = updated_leaders

    updated_followers = []
    for follower in followers:
        if not follower.follow_local_center_of_mass(leaders, followers):
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
    for leader in leaders:
        canvas.create_oval(leader.y * cell_size, leader.x * cell_size, (leader.y + 1) * cell_size, (leader.x + 1) * cell_size, fill='red')
    for follower in followers:
        canvas.create_oval(follower.y * cell_size, follower.x * cell_size, (follower.y + 1) * cell_size, (follower.x + 1) * cell_size, fill='blue')


def animate():
    update()
    canvas.delete("all")
    draw_grid(canvas)
    canvas.after(100, animate)  # Adjust the animation speed by changing the delay time

# Tkinter setup
initialise()
root = tk.Tk()
root.title("Panic Simulation")
canvas = tk.Canvas(root, width=grid_size * cell_size, height=grid_size * cell_size)
canvas.pack()

# Start animation
animate()

root.mainloop()
