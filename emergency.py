import pycxsimulator
from pylab import *

n = 1000  # number of agents
exits = [(0.95, 0.5)]  # location of exits, here one exit at middle of the right wall
speed = 0.01  # maximum movement speed of an agent per step

class agent:
    pass

def initialize():
    global agents
    agents = []
    for i in range(n):
        ag = agent()
        ag.x = random() * 0.9  # ensure agents start inside the building
        ag.y = random()
        agents.append(ag)
    
def observe():
    global agents
    cla()
    scatter([ag.x for ag in agents], [ag.y for ag in agents], color='b', s=8)
    scatter([e[0] for e in exits], [e[1] for e in exits], color='r', s=40, marker='s')
    axis('image')
    axis([0, 1, 0, 1])
    title('Evacuation Model')

def update():
    global agents
    for ag in agents:
        closest_exit = min(exits, key=lambda e: (ag.x - e[0])**2 + (ag.y - e[1])**2)
        move_toward_exit(ag, closest_exit)

def move_toward_exit(ag, exit):
    # Calculate vector toward the exit
    vec_x, vec_y = exit[0] - ag.x, exit[1] - ag.y
    distance = sqrt(vec_x**2 + vec_y**2)
    step_x, step_y = speed * vec_x / distance, speed * vec_y / distance

    # Update position
    ag.x, ag.y = ag.x + step_x, ag.y + step_y

pycxsimulator.GUI().start(func=[initialize, observe, update])
