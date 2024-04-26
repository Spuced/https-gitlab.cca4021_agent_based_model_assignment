import tkinter as tk
import random
import numpy as np

# Constants
open_space = 0
wall = 1
exit = 2
grid_size = 50
cell_size = 16  # Adjust the size of each cell

# Grid setup
grid = [[wall if i == 0 or i == grid_size - 1 or j == 0 or j == grid_size - 1 else open_space for j in range(grid_size)] for i in range(grid_size)]
grid[0][24:26] = [exit, exit]  # Define exit positions


class Leader:
    def __init__(self, velocity):
        self.x = random.randint(1, grid_size - 2)
        self.y = random.randint(1, grid_size - 2)
        self.velocity = velocity

    # def move(self):
    #     potential_moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    #     random.shuffle(potential_moves)
    #     for move_x, move_y in potential_moves:
    #         new_x = self.x + move_x
    #         new_y = self.y + move_y
    #         if 0 <= new_x < grid_size and 0 <= new_y < grid_size:
    #             if grid[new_x][new_y] == exit:
    #                 return True
    #             elif grid[new_x][new_y] == open_space:
    #                 self.x = new_x
    #                 self.y = new_y
    #                 break
    #     return False
    
    def move(self):
        new_x = self.velocity[0]
        new_y = self.velocity[1]
        if 0 <= new_x < grid_size and 0 <= new_y < grid_size:
            self.x += new_x
            self.y += new_y
        else:
            self.x += new_x*-1
            self.y += new_y*-1
    

class Follower:
    def __init__(self):
        self.x = random.randint(1, grid_size - 2)
        self.y = random.randint(1, grid_size - 2)

    def follow_leader(self, leader):
        dx = leader.x - self.x
        dy = leader.y - self.y
        distance = np.sqrt(dx**2 + dy**2)
        if distance > 0:
            self.x += dx / distance
            self.y += dy / distance

def initialise():
    global leaders, followers
    leaders = [Leader(np.random.uniform(-1, 1, 2)) for _ in range(10)]
    followers = [Follower() for _ in range(50)]


def update():
    for leader in leaders:
            leader.move()
    for follower in followers:
        closest_leader = min(leaders, key=lambda leader: np.sqrt((leader.x - follower.x)**2 + (leader.y - follower.y)**2))
        follower.follow_leader(closest_leader)

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
    canvas.after(10, animate)  # Adjust the animation speed by changing the delay time

# Tkinter setup
initialise()
root = tk.Tk()
root.title("Panic Simulation")
canvas = tk.Canvas(root, width=grid_size * cell_size, height=grid_size * cell_size)
canvas.pack()

# Start animation
animate()

root.mainloop()
