import numpy as np
import random
import tkinter as tk

# Create a 100x100 matrix of zeros
matrix = np.zeros((100, 100))

# Set every 10th row and column as road
matrix[::10, :] = 1
matrix[:, ::20] = 1
matrix[99, :] = 1
matrix[:, 99] = 1

# Initialise parameters
num_cars = 10  # Number of cars
car_positions = []

# Place cars at random road positions
while len(car_positions) < num_cars:
    x, y = random.randint(0, 99), random.randint(0, 99)
    if matrix[x, y] == 1:
        car_positions.append((x, y))

def valid_move(x, y):
    return 0 <= x < 100 and 0 <= y < 100 and matrix[x, y] == 1

def move_cars():
    new_positions = []
    for x, y in car_positions:
        possible_moves = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        random.shuffle(possible_moves)
        for new_x, new_y in possible_moves:
            if valid_move(new_x, new_y) and (new_x, new_y) not in new_positions:
                new_positions.append((new_x, new_y))
                break
        else:
            new_positions.append((x, y))
    return new_positions

def update_positions():
    global car_positions
    car_positions = move_cars()
    draw_grid()
    root.after(250, update_positions)  # Update every 250 milliseconds

def draw_grid():
    canvas.delete("all")  # Clear the canvas
    cell_width = cell_height = 15
    for i in range(100):
        for j in range(100):
            color = 'white' if matrix[i, j] == 0 else 'black'
            canvas.create_rectangle(j*cell_width, i*cell_height,
                                    (j+1)*cell_width, (i+1)*cell_height, 
                                    fill=color, outline=color)
    for x, y in car_positions:
        canvas.create_rectangle(y*cell_width, x*cell_height,
                                (y+1)*cell_width, (x+1)*cell_height,
                                fill='red', outline='red')

# Tkinter setup
root = tk.Tk()
root.title("Road Network Simulation")

canvas = tk.Canvas(root, width=2000, height=2000, bg='white')
canvas.pack()

update_positions()  # Start the animation loop
root.mainloop()
