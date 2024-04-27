import numpy as np
import matplotlib.pyplot as plt
from pylab import *

class Agent:
    def __init__(self):
        self.x = rand(2)
        self.x = [np.random.uniform(0, 100), np.random.uniform(0, 100)]
        self.v = rand(2) - array([0.5, 0.5])
        self.vx = [self.x[0]]
        self.vy = [self.x[1]]

    def accelerate(self, agents):
        c = mean([a.x for a in agents])
        f = 0.5 * (c - self.x) / norm(c - self.x) 
        self.v += f # accelerating toward the center of mass
    def move(self):
        self.x += self.v
        self.vx.append(self.x[0])
        self.vy.append(self.x[1])
        if len(self.vx) > 10:
            del self.vx[0]
            del self.vy[0]

class Swarm:
    def __init__(self, num_agents, width, height):
        self.agents = [Agent() for _ in range(num_agents)]
        self.width = width
        self.height = height

    def step(self):
        for a in self.agents:
            a.accelerate(self.agents)
        for a in self.agents:
            a.move()

def visualize(swarm):
    plt.clf()
    plt.xlim(0, swarm.width)
    plt.ylim(0, swarm.height)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.title('Swarm Simulation')

    for agent in swarm.agents:
        plt.plot(agent.x[0], agent.x[1], 'bo')

    plt.pause(0.01)  # Pause to allow time for the plot to be displayed

def main():
    num_agents = 50
    width = 100
    height = 100
    swarm = Swarm(num_agents, width, height)

    # Enable interactive mode
    plt.ion()

    # Create the initial plot
    plt.figure()

    # Simulation loop
    num_steps = 100
    for step in range(num_steps):
        swarm.step()
        visualize(swarm)

    # Turn off interactive mode after the simulation is complete
    plt.ioff()
    plt.show()

if __name__ == "__main__":
    main()
