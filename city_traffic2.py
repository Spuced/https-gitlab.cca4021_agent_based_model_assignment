import numpy as np
import pycxsimulator
from pylab import *

# Constants for the simulation
width = 60
height = 60
populationSize = 30  # Number of cars

free = 0
road = 1

# Create a 60x60 matrix with designated roads
envir = np.zeros((height, width))
envir[::15, :] = road
envir[:, ::20] = road
envir[59, :] = road
envir[:, 59] = road

def initialize():
    global time, agents

    time = 0
    agents = []
    for _ in range(populationSize):
        # Place new agents randomly on the road
        while True:
            x, y = randint(width), randint(height)
            if envir[y, x] == road:
                agents.append([x, y])
                break

def observe():
    cla()  # Clear the current axes
    # Display the road matrix
    imshow(envir, cmap='gray', vmin=0, vmax=1, alpha=0.8)  # Alpha for transparency to see agents better
    axis('image')  # Ensures no distortion in the aspect ratio
    scatter([ag[0] for ag in agents], [ag[1] for ag in agents], c='blue', s=50)  # s is size of the scatter dots
    title('t = ' + str(time))


def update():
    global time, agents

    time += 1

    for ag in agents:
        direction = randint(4)
        if direction == 0 and ag[0] > 0 and envir[ag[1], ag[0]-1] == road:  # left
            ag[0] -= 1
        elif direction == 1 and ag[0] < width - 1 and envir[ag[1], ag[0]+1] == road:  # right
            ag[0] += 1
        elif direction == 2 and ag[1] > 0 and envir[ag[1]-1, ag[0]] == road:  # up
            ag[1] -= 1
        elif direction == 3 and ag[1] < height - 1 and envir[ag[1]+1, ag[0]] == road:  # down
            ag[1] += 1

pycxsimulator.GUI().start(func=[initialize, observe, update])
