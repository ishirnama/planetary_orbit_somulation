import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import os
print("Current working directory:", os.getcwd())

# -------------------------------------------------------
# Constants (using AU, Earth mass, Earth year units)
# -------------------------------------------------------

G = 4 * np.pi**2 / 332946   # In units AU^3 / (Earth mass * year^2)

DT = 0.001         # timestep (years)
TOTAL_TIME = 12    # simulate 12 years (enough for Jupiter)

ENERGY_OUTPUT_FILE = "energy_output.txt"


# -------------------------------------------------------
# Body Class
# -------------------------------------------------------

class Body:
    def __init__(self, name, mass, orbital_radius, colour):
        self.name = name
        self.mass = mass
        self.colour = colour
        

        # Initial position x₀ = [R, 0] (where R is the orbital radius)
        self.position = np.array([orbital_radius, 0.0])

        # Initial velocity (positive y direction)
        # if we have a +ive orbital radius,
        if orbital_radius > 0:
            # find the velocity vector using the orbital velocity formula
            v = np.sqrt(G * bodies_dict["sun"].mass / orbital_radius)   # v = sqrt(G * M / R) for circular orbit
            # assign this velocity vector to the body's velocity attribute
            self.velocity = np.array([0.0, v])
        # if we have -ive orbital radius, this is not possible ; so we set the velocity to zero.
        else:
            # assign this zero vector to the body's velocity attribute
            self.velocity = np.array([0.0, 0.0])
        # setting the initial acceleration to zero
        self.acceleration = np.array([0.0, 0.0])
        # setting the previous acceleration to zero
        self.prev_acceleration = np.array([0.0, 0.0])

        # creating an attribute for orbital period (T)
        self.orbital_period = None
        # creating an attribute for detecting wether the body completes a full orbit
        self.crossed_positive_x = False
        # creating an attribute to store the time of the last completion of the orbit
        self.last_crossing_time = None
        # creating an attribute to store yₙ₋₁ (the y position in the previous timestep)
        self.prev_y = self.position[1]


# -------------------------------------------------------
# Simulation Class
# -------------------------------------------------------

class NBodySimulation:
    def __init__(self, filename):
        self.bodies = self.load_bodies(filename)
        self.time = 0.0

        self.calculate_accelerations()

        # Store previous acceleration for Beeman
        for body in self.bodies:
            body.prev_acceleration = body.acceleration.copy()

    def load_bodies(self, filename):
        with open(filename) as f:
            data = json.load(f)

        bodies = []
        global bodies_dict
        bodies_dict = {}

        for entry in data["bodies"]:
            body = Body(entry["name"],
                        entry["mass"],
                        entry["orbital_radius"],
                        entry["colour"])
            bodies.append(body)
            bodies_dict[body.name] = body
            print(entry["name"]) # <-- debug print to verify body loading.
        
        return bodies

    # ---------------------------------------------------
    # Gravitational acceleration
    # ---------------------------------------------------

    def calculate_accelerations(self):
        for body in self.bodies:
            total_force = np.zeros(2)
            for other in self.bodies:
                if body is not other:
                    r_vec = body.position - other.position
                    r = np.linalg.norm(r_vec)
                    total_force += -G * other.mass * r_vec / r**3
            body.acceleration = total_force

    # ---------------------------------------------------
    # Beeman Integration
    # ---------------------------------------------------

    def step(self):
        # Update positions
        for body in self.bodies:
            body.position += (
                body.velocity * DT
                + (2/3) * body.acceleration * DT**2
                - (1/6) * body.prev_acceleration * DT**2
            )

        # Store old accelerations
        old_accelerations = [body.acceleration.copy() for body in self.bodies]

        # Recalculate accelerations
        self.calculate_accelerations()

        # Update velocities
        for i, body in enumerate(self.bodies):
            body.velocity += (
                (1/3) * body.acceleration * DT
                + (5/6) * old_accelerations[i] * DT
                - (1/6) * body.prev_acceleration * DT
            )
            body.prev_acceleration = old_accelerations[i]

        self.time += DT

        self.detect_orbits()

    # ---------------------------------------------------
    # Orbital Period Detection
    # ---------------------------------------------------

    def detect_orbits(self):
        for body in self.bodies:
            if body.name == "sun":
                continue

            x, y = body.position
            vx, vy = body.velocity

            # Detect crossing of x-axis from negative y to positive y
            if body.prev_y < 0 and y >= 0 and vx > 0:

                if body.last_crossing_time is not None:
                    period = self.time - body.last_crossing_time
                    print(f"{body.name} orbital period: {period:.3f} Earth years")

                body.last_crossing_time = self.time

            body.prev_y = y

    # ---------------------------------------------------
    # Energy Calculation
    # ---------------------------------------------------

    def total_energy(self):
        kinetic = 0.0
        potential = 0.0

        for body in self.bodies:
            kinetic += 0.5 * body.mass * np.dot(body.velocity, body.velocity)

        for i in range(len(self.bodies)):
            for j in range(i + 1, len(self.bodies)):
                r = np.linalg.norm(self.bodies[i].position -
                                   self.bodies[j].position)
                potential += -G * self.bodies[i].mass * \
                             self.bodies[j].mass / r

        return kinetic + potential


# -------------------------------------------------------
# Run Simulation
# -------------------------------------------------------

simulation = NBodySimulation("parameters_solar.json")

positions_history = {body.name: [] for body in simulation.bodies}

with open(ENERGY_OUTPUT_FILE, "w") as f_energy:

    steps = int(TOTAL_TIME / DT)

    for _ in range(steps):
        simulation.step()

        for body in simulation.bodies:
            positions_history[body.name].append(body.position.copy())

        if int(simulation.time / DT) % 10 == 0:
            f_energy.write(f"{simulation.time} "
                           f"{simulation.total_energy()}\n")

# -------------------------------------------------------
# Animation
# -------------------------------------------------------

fig, ax = plt.subplots()
ax.set_aspect("equal")
ax.set_xlim(-6, 6)
ax.set_ylim(-6, 6)

lines = {}
for body in simulation.bodies:
    line, = ax.plot([], [], 'o', color=body.colour, markersize=6, label=body.name)
    ax.legend()
    lines[body.name] = line


def update(frame):
    for body in simulation.bodies:
        pos = positions_history[body.name][frame]
        lines[body.name].set_data([pos[0]], [pos[1]])
    return list(lines.values())


ani = FuncAnimation(fig, update,
                    frames=len(positions_history["earth"]),
                    interval=20, blit=True)

plt.show()