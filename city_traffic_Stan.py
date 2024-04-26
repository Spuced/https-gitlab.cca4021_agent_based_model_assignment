import numpy as np
import random
import tkinter as tk

# Create a 60x60 matrix of zeros
matrix = np.zeros((60, 60))

# Set every 15th row and column as road
matrix[::15, :] = 1
matrix[:, ::15] = 1

# Define bus stop locations
bus_stops = [(2, 0), (2, 15), (2, 30), (2, 45), (17, 0), (17, 15), (17, 30), (17, 45)]

# Define bus route
bus_route = [(2, j) for j in range(0, 60, 15)]

# Initialize parameters
num_cars = 20  # Number of cars
num_pedestrians = 10  # Number of pedestrians

car_agents = []  # List to store car agents (position, directions)
pedestrian_agents = []  # List to store pedestrian agents (position, directions)

# Place cars at random road positions
while len(car_agents) < num_cars:
    x, y = random.randint(0, 59), random.randint(0, 59)
    if matrix[x, y] == 1:
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Initial random directions
        random.shuffle(directions)
        car_agents.append(((x, y), directions))

# Place pedestrians at random road positions
while len(pedestrian_agents) < num_pedestrians:
    x, y = random.randint(0, 59), random.randint(0, 59)
    if matrix[x, y] == 1:
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Initial random directions
        random.shuffle(directions)
        pedestrian_agents.append(((x, y), directions))

def valid_move(x, y):
    return 0 <= x < 60 and 0 <= y < 60 and matrix[x, y] == 1

def move_agents(agents):
    new_positions = []
    for (x, y), directions in agents:
        if len(directions) == 0:
            continue  # Agent has reached its destination
        dx, dy = directions[0]
        new_x, new_y = x + dx, y + dy
        if valid_move(new_x, new_y):
            new_positions.append(((new_x, new_y), directions[1:]))
        else:
            # If the next move is invalid, choose a new random direction
            random.shuffle(directions)
            new_positions.append(((x, y), directions))
    return new_positions

def update_positions():
    global car_agents, pedestrian_agents
    
    # Move cars
    car_agents = move_agents(car_agents)
    
    # Move pedestrians towards bus stops
    for i, ((x, y), directions) in enumerate(pedestrian_agents):
        if (x, y) in bus_stops:
            continue  # Pedestrian is already at a bus stop
        nearest_stop = min(bus_stops, key=lambda pos: abs(pos[0] - x) + abs(pos[1] - y))
        dx = 1 if nearest_stop[0] > x else (-1 if nearest_stop[0] < x else 0)
        dy = 1 if nearest_stop[1] > y else (-1 if nearest_stop[1] < y else 0)
        pedestrian_agents[i] = (((x + dx, y + dy), directions))

    draw_grid()
    root.after(1000, update_positions)  # Update every second

def draw_grid():
    canvas.delete("all")  # Clear the canvas
    cell_width = cell_height = 15
    for i in range(60):
        for j in range(60):
            color = 'white' if matrix[i, j] == 0 else 'black'
            canvas.create_rectangle(j*cell_width, i*cell_height,
                                    (j+1)*cell_width, (i+1)*cell_height, 
                                    fill=color, outline=color)
    for (x, y), _ in car_agents:
        canvas.create_rectangle(y*cell_width, x*cell_height,
                                (y+1)*cell_width, (x+1)*cell_height,
                                fill='red', outline='red')
    for (x, y), _ in pedestrian_agents:
        canvas.create_oval(y*cell_width, x*cell_height,
                           (y+1)*cell_width, (x+1)*cell_height,
                           fill='blue', outline='blue')
    for x, y in bus_route:
        canvas.create_rectangle(y*cell_width, x*cell_height,
                                (y+1)*cell_width, (x+1)*cell_height,
                                fill='green', outline='green')

# Tkinter setup
root = tk.Tk()
root.title("Road Network Simulation")

canvas = tk.Canvas(root, width=900, height=900, bg='white')
canvas.pack()

update_positions()  # Start the animation loop
root.mainloop()
