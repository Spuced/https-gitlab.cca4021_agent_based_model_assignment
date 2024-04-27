import numpy as np
import matplotlib.pyplot as plt

class CelestialBody:
    def __init__(self, mass, position, velocity):
        self.mass = mass
        self.position = np.array(position)
        self.velocity = np.array(velocity)

    def update_position(self, dt):
        self.position += self.velocity * dt

def compute_gravitational_force(body1, body2):
    G = 6.67430e-11  # gravitational constant in m^3 kg^-1 s^-2
    r_vec = body2.position - body1.position
    r_mag = np.linalg.norm(r_vec)
    r_hat = r_vec / r_mag
    force_mag = G * body1.mass * body2.mass / r_mag**2
    return force_mag * r_hat

def update_system(bodies, dt):
    n = len(bodies)
    forces = [np.zeros(3) for _ in bodies]
    for i in range(n):
        for j in range(i + 1, n):
            force = compute_gravitational_force(bodies[i], bodies[j])
            forces[i] += force / bodies[i].mass
            forces[j] -= force / bodies[j].mass
    for i, body in enumerate(bodies):
        body.velocity += forces[i] * dt
        body.update_position(dt)

# Example initialization and simulation loop
bodies = [
    CelestialBody(mass=1e24, position=[1e11, 0, 0], velocity=[0, 1000, 0]),
    CelestialBody(mass=1e24, position=[-1e11, 0, 0], velocity=[0, -1000, 0])
]

dt = 1.0  # time step in seconds
for _ in range(10000):
    update_system(bodies, dt)
    # Optional: Plot positions here or update your visualization
