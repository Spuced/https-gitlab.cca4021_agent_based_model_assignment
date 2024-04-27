import numpy as np
import matplotlib.pyplot as plt

class Leader:
    def __init__(self, x, y, velocity):
        self.x = x
        self.y = y
        self.velocity = velocity

    def move(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]

class Follower:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def follow_leader(self, leader):
        dx = leader.x - self.x
        dy = leader.y - self.y
        distance = np.sqrt(dx**2 + dy**2)
        if distance > 0:
            self.x += dx / distance
            self.y += dy / distance


def initialise():
    global leaders, followers, width, height
    width = 100
    height = 100
    leaders = [Leader(np.random.uniform(0, width), np.random.uniform(0, height), np.random.uniform(-1, 1, 2)) for _ in range(50)]
    followers = [Follower(np.random.uniform(0, width), np.random.uniform(0, height)) for _ in range(300)]

def observe():
    plt.clf()
    plt.xlim(0, width)
    plt.ylim(0, height)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.title('Swarm Simulation')

    for leader in leaders:
        plt.plot(leader.x, leader.y, 'ro')
    for follower in followers:
        plt.plot(follower.x, follower.y, 'bo')

    plt.pause(0.01)

def update():
    for leader in leaders:
            leader.move()
    for follower in followers:
        closest_leader = min(leaders, key=lambda leader: np.sqrt((leader.x - follower.x)**2 + (leader.y - follower.y)**2))
        follower.follow_leader(closest_leader)



initialise()

plt.ion()
plt.figure()

num_steps = 100
for step in range(num_steps):
    update()
    observe()

plt.ioff()
plt.show()

