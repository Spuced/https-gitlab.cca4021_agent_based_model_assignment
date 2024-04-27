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

    def follow_leader(self, leader):
        potential_moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        moves = []
        [moves.append(np.sqrt(((leader.x-(self.x+move_x))**2 + (leader.y-(self.y+move_y))**2))) for move_x, move_y in potential_moves]
        dist = min(moves)
        index = moves.index(dist)
        move = potential_moves[index]
        move_x, move_y = move
        new_x = self.x + move_x
        new_y = self.y + move_y
        if 0 <= new_x < grid_size and 0 <= new_y < grid_size:
            if grid[new_x][new_y] == exit:
                return True
            elif grid[new_x][new_y] == open_space:
                self.x = new_x
                self.y = new_y
        return False

def initialise():
    global leaders, followers
    leaders = [FireWarden() for _ in range(2)]
    followers = [Follower() for _ in range(50)]


def update():
    for leader in leaders:
            if not leader.move():
                leader
    for follower in followers:
        closest_leader = min(leaders, key=lambda leader: np.sqrt((leader.x - follower.x)**2 + (leader.y - follower.y)**2))
        if not follower.follow_leader(closest_leader):
            follower

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
