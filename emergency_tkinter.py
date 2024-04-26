import tkinter as tk
import random

# Constants
open_space = 0
wall = 1
exit = 2
grid_size = 100
cell_size = 16  # Adjust the size of each cell

# Grid setup
grid = [[wall if i == 0 or i == grid_size - 1 or j == 0 or j == grid_size - 1 else open_space for j in range(grid_size)] for i in range(grid_size)]
grid[0][49:51] = [exit, exit]  # Define exit positions

class Panicker:
    def __init__(self):
        self.x = random.randint(1, grid_size - 2)
        self.y = random.randint(1, grid_size - 2)

    def move(self):
        potential_moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        random.shuffle(potential_moves)
        for move_x, move_y in potential_moves:
            new_x = self.x + move_x
            new_y = self.y + move_y
            if 0 <= new_x < grid_size and 0 <= new_y < grid_size:
                if grid[new_x][new_y] == exit:
                    return True
                elif grid[new_x][new_y] == open_space:
                    self.x = new_x
                    self.y = new_y
                    break
        return False

def initialise():
    global panickers
    panickers = [Panicker() for _ in range(100)]

def update():
    global panickers
    panickers = [panicker for panicker in panickers if not panicker.move()]

def draw_grid(canvas):
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i][j] == wall:
                canvas.create_rectangle(j * cell_size, i * cell_size, (j + 1) * cell_size, (i + 1) * cell_size, fill='black')
            elif grid[i][j] == exit:
                canvas.create_rectangle(j * cell_size, i * cell_size, (j + 1) * cell_size, (i + 1) * cell_size, fill='green')
    for panicker in panickers:
        canvas.create_oval(panicker.y * cell_size, panicker.x * cell_size, (panicker.y + 1) * cell_size, (panicker.x + 1) * cell_size, fill='red')

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
