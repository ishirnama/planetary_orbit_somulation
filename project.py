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

dt = 0.001         # timestep (years)
TOTAL_TIME = 12    # simulate 12 years (enough for Jupiter)

ENERGY_OUTPUT_FILE = "energy_output.txt"


# -------------------------------------------------------
# Body Class
# -------------------------------------------------------

class Body:
    def __init__(self, name, mass, orbital_radius, colour):
        # name of the bodye
        self.name = name
        # mass of the body (mᵢ)
        self.mass = mass
        # color of the body (according to the JSON file)
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
        # creating an attribute for holding the data in the JSON file after opening it
        self.bodies = self.load_bodies(filename)
        # creating an attribute for the run-time of the simulation (t)
        self.time = 0.0
        # creating an attribute for the accelerations of the bodies (a)
        self.calculate_accelerations()

        # Store previous acceleration for Beeman
        for body in self.bodies:
            # coping the current acceleration of the body into it's previous acceleration attirbute
            body.prev_acceleration = body.acceleration.copy()
    
    # loading the data from the JSON file and creating Body objects for each entry in the "bodies" list in the JSON file,
    # then storing these Body objects in a list and a dictionary for easy access.
    def load_bodies(self, filename):
        # opening the JSON file with the filename as an input parameter
        with open(filename) as f:
            # loading the data from the JSON file into a variable called "data"
            data = json.load(f)

        # creating an empty list called "bodies" to store the Body objects
        bodies = []
        # creating an empty dictionary called "bodies_dict" to store the Body objects with respect to their names as the keys.
        global bodies_dict
        bodies_dict = {}

        # itterating through each entry in data (loaded from the JSON) and creating a Body object for each one
        for entry in data["bodies"]:
            body = Body(entry["name"],
                        entry["mass"],
                        entry["orbital_radius"],
                        entry["colour"])
            # appending the Body object to the bodies list
            bodies.append(body)
            # storing the Body object in the bodies_dict dictionary with the name of the body as a key
            bodies_dict[body.name] = body
            # printing the name of the body to make sure they all load properly
            print(entry["name"]) # <-- debug print to verify body loading.
        # returning the list of Body objects
        return bodies

    # ---------------------------------------------------
    # Gravitational acceleration
    # ---------------------------------------------------

    def calculate_accelerations(self):
        # for each j-th Body object in the bodies list
        for body in self.bodies:
            # create an acceleration vector (aⱼᵢ) and assign it to zero
            a = np.zeros(2)
            # now for each i-th Body object in the bodies list,
            for other in self.bodies:
                # if our j-th body is not our i-th body,
                if body is not other:
                    # calculate the position vector from the i-th body to the j-th body (rᵢⱼ = rᵢ - rⱼ)
                    r_vec = body.position - other.position
                    # calculate the magnitude of this position vector (r = |rᵢⱼ|)
                    r = np.linalg.norm(r_vec)
                    # Use the simplified gravitational force formula 
                    '''
                               mᵢ mⱼ
                    Fⱼᵢ = -G __________ rⱼᵢ(t)
                              |rⱼᵢ(t)|³
                        
                           ∂Fⱼᵢ
                    aⱼᵢ = _____
                           ∂mⱼ

                                 mᵢ
                        = -G __________ rⱼᵢ(t)
                              |rⱼᵢ(t)|³
                
                    where G is the gravitational constant, mᵢ and mⱼ are the masses of the i-th and j-th bodies, and rᵢⱼ is the position vector from body j to body i.
                    '''
                    # to update the accelereation vector of the j-th body (aⱼᵢ)
                    a += ((-G * other.mass) / r**3) * r_vec
            body.acceleration = a

    # ---------------------------------------------------
    # Beeman Integration
    # ---------------------------------------------------

    def step(self):
        # Update positions
        # going through each body's position
        for body in self.bodies:
            # r(t+δt) = r(t) + v(t)·δt + ([ 4a(t) - a(t-δt) ]/6)·δt²
            # ∴ r(t+δt) - r() = v(t)·δt + ([ 4a(t) - a(t-δt) ]/6)·δt²
            # ∴ δr = v(t)·δt + ([ 4a(t) - a(t-δt) ]/6)·δt
            # and to update position we just have to do r(t)+=δr as done below
            body.position += (body.velocity*dt + (2/3)*body.acceleration*(dt**2) - (1/6)*body.prev_acceleration*(dt**2))

        # Store old accelerations
        old_accelerations = [body.acceleration.copy() for body in self.bodies]

        # Recalculate accelerations
        self.calculate_accelerations()

        # Update velocities
        # going through each bodie's velocity
        for i, body in enumerate(self.bodies):
            # v(t+δt) = v(t) + ([ 2a(t+δt) + 5a(t) - a(t - δt) ]/6)·δt
            # ∴ v(t+δt) - v(t) = ([ 2a(t+δt) + 5a(t) - a(t - δt) ]/6)·δt
            # ∴ δv = ([ 2a(t+δt) + 5a(t) - a(t - δt) ]/6)·δt
            # and to update velocity we just have to do v(t)+=δv as done below
            body.velocity += ((1/3)*body.acceleration*dt + (5/6)*old_accelerations[i]*dt - (1/6)*body.prev_acceleration*dt)
            # storing the current acceleration into the old accelerations list for the next timestep
            body.prev_acceleration = old_accelerations[i]
        
        # updating the timestep (t + δt)
        self.time += dt
        # checking if the body completed a full orbit
        self.detect_orbits()

    # ---------------------------------------------------
    # Orbital Period Detection
    # ---------------------------------------------------

    # function to detect the amount of time each body takes to cross the x-axis
    def detect_orbits(self):
        # iterating through each body in the bodies list
        for body in self.bodies:
            # if the body is the sun,
            if body.name == "sun":
                # we skip it (we're assuming it stays in a fixed position at the origin)
                continue

            # spliting the position vector into x and y components
            x, y = body.position
            # splitting the velocity vector into x and y components (vₓ and vᵧ)
            vx, vy = body.velocity

            # Detect crossing of x-axis from negative y to positive y
            # if y(t-δt) < 0 and y(t) >= 0 and vₓ > 0, then we have a crossing of the x-axis
            if body.prev_y < 0 and y >= 0 and vx > 0:

                # if this body has already crossed the x-axis before
                if body.last_crossing_time is not None:
                    # the period is the difference between the time it crosses before and the time right now
                    period = self.time - body.last_crossing_time
                    # printing the orbital period
                    print(f"{body.name} orbital period: {period:.3f} Earth years")
                # adjusting the last crossing time to the current time (t)
                body.last_crossing_time = self.time
            # adjusting the previous-y to the current-y for the next timestep
            body.prev_y = y

    # ---------------------------------------------------
    # Energy Calculation
    # ---------------------------------------------------

    def total_energy(self):
        # setting T₀ = 0
        T = 0.0
        # setting V₀ = 0
        V = 0.0

        # going through each body
        for body in self.bodies:
            # calculating the kinetic energy of the body (Tᵢ = 0.5 * mᵢ * vᵢ²) at that point
            T += 0.5 * body.mass * np.dot(body.velocity, body.velocity)
        # for each iteration in the bodies list,
        for i in range(len(self.bodies)):
            # for each iteration of the bodies excluding the i-th body,
            for j in range(i + 1, len(self.bodies)):
                # calculating |r_ij| = |rᵢ - rⱼ|
                r = np.linalg.norm(self.bodies[i].position - self.bodies[j].position)
                # calculating the gravitational potential energy (Vᵢⱼ)
                V += (-G * self.bodies[i].mass * self.bodies[j].mass) / r
        # returning the total energy ∑E
        return T + V


# -------------------------------------------------------
# Run Simulation
# -------------------------------------------------------

# loading the class to simulate all the planets (including the sun)
simulation = NBodySimulation("parameters_solar.json")

# creating empty lists for the position histories of the bodies
positions_history = {body.name: [] for body in simulation.bodies}

# opening a text file to store the total energy for each timestep
with open(ENERGY_OUTPUT_FILE, "w") as f_energy:
    # calculate the total number of steps for this simulation
    steps = int(TOTAL_TIME / dt)
    # after each step,
    for _ in range(steps):
        # do the simulation
        simulation.step()
        # for each body in the bodies list,
        for body in simulation.bodies:
            # putting xₜ into the list of position histories
            positions_history[body.name].append(body.position.copy())
        # every 10 steps,
        if int(simulation.time / dt) % 10 == 0:
            # write the current time and total energy into the energy file (f_energy)
            f_energy.write(f"{simulation.time} "f"{simulation.total_energy()}\n")

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