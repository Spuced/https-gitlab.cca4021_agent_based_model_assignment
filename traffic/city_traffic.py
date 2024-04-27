import numpy as np
import random
import tkinter as tk

# Create a 100x100 matrix of zeros
matrix = np.zeros((60, 60))

# Set every 10th row and column as road
matrix[::15, :] = 1
matrix[:, ::20] = 1
matrix[59, :] = 1
matrix[:, 59] = 1

# Initialise parameters
num_cars = 20  # Number of cars
car_positions = []  # List to store current positions
last_moves = {}  # Dictionary to store the last move direction of each car

# Place cars at random road positions
while len(car_positions) < num_cars:
    x, y = random.randint(0, 59), random.randint(0, 59)
    if matrix[x, y] == 1:
        car_positions.append((x, y))
        last_moves[(x, y)] = None

def valid_move(x, y):
    return 0 <= x < 60 and 0 <= y < 60 and matrix[x, y] == 1

def move_cars():
    new_positions = []
    new_moves = {}
    for x, y in car_positions:
        possible_moves = [(x-1, y, 'up'), (x+1, y, 'down'), (x, y-1, 'left'), (x, y+1, 'right')]
        random.shuffle(possible_moves)  # Shuffle to randomize the move order
        last_move = last_moves.get((x, y))
        if last_move:
            # Avoid the reverse of the last move if possible
            reverse_moves = {'up': 'down', 'down': 'up', 'left': 'right', 'right': 'left'}
            preferred_moves = [move for move in possible_moves if move[2] != reverse_moves[last_move]]
            if preferred_moves:
                possible_moves = preferred_moves
        for new_x, new_y, move in possible_moves:
            if valid_move(new_x, new_y) and (new_x, new_y) not in new_positions:
                new_positions.append((new_x, new_y))
                new_moves[(new_x, new_y)] = move
                break
        else:
            new_positions.append((x, y))
            new_moves[(x, y)] = last_moves.get((x, y))
    return new_positions, new_moves

def update_positions():
    global car_positions, last_moves
    car_positions, last_moves = move_cars()
    draw_grid()
    root.after(1, update_positions)  # Update every 100 milliseconds

def draw_grid():
    canvas.delete("all")  # Clear the canvas
    cell_width = cell_height = 15
    for i in range(60):
        for j in range(60):
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
