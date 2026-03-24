import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# gravitational constant [AU³ M⊕⁻¹ yr⁻²]
G = 4 * np.pi**2 / 332946

# timestep [yr]
dt = 0.001

# simulate 25 years (because Jupiter needs to cross the x-axis at least twice to get an accurate period measurement)
# once at the start (t = 0)
# and once at the end (t = 25)
TOTAL_TIME = 25

# making a file to store the total energy of the system at each timestep
ENERGY_OUTPUT_FILE = "energy_output.txt"


# making a class for each body
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

# creating a class for the whole simulation
class NBodySimulation:
    def __init__(self, filename, method="beeman"):
        # picking the method of integration (the default is beeman)
        self.method = method
        # creating an attribute for holding the data in the JSON file after opening it
        self.bodies = self.load_bodies(filename)
        # creating an attribute for the run-time of the simulation (t)
        self.time = 0.0
        # creating an attribute for the accelerations of the bodies (a)
        self.calculate_accelerations()
        # deciding the color of the total energy graph based on the method of integration
        self.colour = None
        # creating an attribute for the time when all 5 planets align
        self.alignment_time = 0.0

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
        # returning the list of Body objects
        return bodies

    # making a method to update accelerations of the bodies at each timestep
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
            # updating the acceleration attribute of the j-th body
            body.acceleration = a

    # different types of integration methods
    def step(self):
        # if the user picks beeman method
        if self.method == "beeman":
            # call the step function for beemian integration
            self.step_beeman()
            # beeman's graph is blue
            self.colour = "blue"
        # otherwise, if the user picks euler-cromer method
        elif self.method == "euler_cromer":
            #call the step function for euler-cromer integration
            self.step_euler_cromer()
            # euler & cromer's graph is red
            self.colour = "red"
        # otherwise, if the user picks direct-euler method
        elif self.method == "euler":
            # call the step function for direct-euler integration
            self.step_euler()
            # euler's graph is green
            self.colour = "green"
        # updating the timestep (t + δt)
        self.time += dt
        # checking if the body completed a full orbit
        self.detect_orbits()

    def step_beeman(self):
        # update positions
        # going through each body's position
        for body in self.bodies:
            # r(t+δt) = r(t) + v(t)·δt + ([ 4a(t) - a(t-δt) ]/6)·δt²
            # ∴ r(t+δt) - r(t) = v(t)·δt + ([ 4a(t) - a(t-δt) ]/6)·δt²
            # ∴ δr = v(t)·δt + ([ 4a(t) - a(t-δt) ]/6)·δt²
            # and to update position we just have to do r(t)+=δr as done below
            body.position += (body.velocity*dt + (2/3)*body.acceleration*(dt**2) - (1/6)*body.prev_acceleration*(dt**2))

        # store old accelerations
        old_accelerations = [body.acceleration.copy() for body in self.bodies]

        # recalculate accelerations
        self.calculate_accelerations()

        # update velocities
        # going through each bodie's velocity
        for i, body in enumerate(self.bodies):
            # v(t+δt) = v(t) + ([ 2a(t+δt) + 5a(t) - a(t - δt) ]/6)·δt
            # ∴ v(t+δt) - v(t) = ([ 2a(t+δt) + 5a(t) - a(t - δt) ]/6)·δt
            # ∴ δv = ([ 2a(t+δt) + 5a(t) - a(t - δt) ]/6)·δt
            # and to update velocity we just have to do v(t)+=δv as done below
            body.velocity += ((1/3)*body.acceleration*dt + (5/6)*old_accelerations[i]*dt - (1/6)*body.prev_acceleration*dt)
            # storing the current acceleration into the old accelerations list for the next timestep
            body.prev_acceleration = old_accelerations[i]
    
    def step_euler_cromer(self):
        # update velocities
        # going through each body's velocity
        for body in self.bodies:
            # v(t+δt) = v(t) + a(t)·δt
            # ∴ v(t+δt) - v(t) = a(t)·δt
            # ∴ δv = a(t)·δt
            # and to update velocity we just have to do v(t)+=δv as done below
            # here, a(t)·δt is just (δv/δt)·δt which is δv
            # so v(t)+=δv is the same as v(t)+=a(t)·δt as done below
            body.velocity += body.acceleration * dt
        
        # going through each body's position
        for body in self.bodies:
            # r(t+δt) = r(t) + v(t+δt)·δt
            # because the velocity is updated, v(t+δt) is becomes v(t)
            # ∴ r(t+δt) - r(t) = v(t)·δt
            # ∴ δr = v(t)·δt
            # here, v(t)·δt is just (δr/δt)·δt which is δr
            # so r(t)+=δr is the same as r(t)+=v(t)·δt as done below
            body.position += body.velocity * dt

        # recalculate accelerations
        self.calculate_accelerations()
    
    def step_euler(self):
        # Store old velocities
        old_velocities = [body.velocity.copy() for body in self.bodies]
        # going through each body's position
        for i, body in enumerate(self.bodies):
            # r(t+δt) = r(t) + v(t)·δt
            # ∴ r(t+δt) - r(t) = v(t)·δt
            # ∴ δr = v(t)·δt
            # here, v(t)·δt is just (δr/δt)·δt which is δr
            # so r(t)+=δr is the same as r(t)+=v(t)·δt as done below
            body.position += old_velocities[i] * dt

        # going through each body's velocity
        for body in self.bodies:
            # v(t+δt) = v(t) + a(t)·δt
            # ∴ v(t+δt) - v(t) = a(t)·δt
            # ∴ δv = a(t)·δt
            # here, a(t)·δt is just (δv/δt)·δt which is δv
            # so v(t)+=δv is the same as v(t)+=a(t)·δt as done below
            body.velocity += body.acceleration * dt

        # recalculate accelerations
        self.calculate_accelerations()

    # detecting the amount of time each body takes to cross the x-axis
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
                    # storing the period in the orbital_period attribute of the body
                    body.orbital_period = period
                # adjusting the last crossing time to the current time (t)
                body.last_crossing_time = self.time
            # adjusting the previous-y to the current-y for the next timestep
            body.prev_y = y

    # calculating the total energy of the system at a specific time (ΣE(t))
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
        # returning the total energy ∑E(t)
        return T + V
    
    # calculating when the planets align
    def detect_alignment(self, threshold_deg=5):
        # making an empty list to store the angles at specific timesteps θ(t)
        angles = []
        # going through each body,
        for body in self.bodies:
            # if the body is the sun,
            if body.name == "sun":
                # we can ignore it because it's angle to the x-axis is permanently 0
                continue

            # Finding the angle between the position of the body and the x-axis
            #
            #        y      r(t)                        rᵧ
            #         |    /                 tan(θ) =  ____
            #         |   /                             rₓ
            #         |  /
            #         | /                    ∴    θ = arctan(rᵧ / rₓ)
            #      ___|/θ)___ x
            #         |
            #
            angle = np.arctan2(body.position[1], body.position[0])
            # putting the angle into the angles list
            angles.append(angle)
        # making it a numpy array so that each planet's 
        angles = np.array(angles)
        
        # polar coordinates : 
        # x = r·cos(θ) & y = r·sin(θ) where r = 1 ,     (becuz unit vector)
        # making a collection of unit vectors for every θ(t)
        unit_vectors = np.column_stack((np.cos(angles), np.sin(angles)))

        # finding μ(t) the mean vector at a specific instance in time for all bodies
        mean_vector = np.mean(unit_vectors, axis=0)

        # finding θₘ(t) the angle of the mean vector
        mean_angle = np.arctan2(mean_vector[1], mean_vector[0])

        # finding δθ = |arctan(sin(θ - θₘ) / cos(θ - θₘ))|
        # which gives the angle between μ(t) and r(t) for each bopdy
        diffs = np.abs(np.arctan2(np.sin(angles - mean_angle), np.cos(angles - mean_angle)))
        # converting the threshold angle (φ) into radians because that's what the difference angles are in
        threshold = np.deg2rad(threshold_deg)
        # comparing δθ with φ
        if np.all(diffs < threshold):
            # δθ < φ for all bodies, then all of their r(t)'s are super close to μ(t) and thus they are all aligned with each other
            print(f"Alignment at t = {self.time:.3f} years")
            # updating the alignment time
            self.alignment_time = self.time

if __name__ == "__main__":
    # Integration options :
    # - "beeman"
    # - "euler_cromer"
    # - "euler"

    # loading the class to simulate all the planets (and the sun too)
    simulation = NBodySimulation("parameters_solar.json")

    # creating empty lists for the position histories of the bodies
    positions_history = {body.name: [] for body in simulation.bodies}

    # total energy for the system list
    energy_history = []
    # every-10-timesteps for the system list
    time_history = []

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
            # locally storing total energy every 10 steps for plotting a nice graph
            energy_history.append(simulation.total_energy())
            # locally storing the time every 10 steps
            time_history.append(simulation.time)


    # animating the planets orbiting the sun
    fig, ax = plt.subplots()
    ax.set_aspect("equal")
    ax.set_xlim(-6, 6)
    ax.set_ylim(-6, 6)

    lines = {}
    for body in simulation.bodies:
        line, = ax.plot([], [], 'o', color=body.colour, markersize=6, label=body.name)
        ax.set_xlabel("x [AU]")
        ax.set_ylabel("y [AU]")
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