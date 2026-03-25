import simulation

if __name__ == "__main__":
    
    # simulate 25 years (because Jupiter needs to cross the x-axis at least twice to get an accurate period measurement)
    # once at the start (t = 0)
    # and once at the end (t = 25)
    TOTAL_TIME = 25

    # making a file to store the total energy of the system at each timestep
    ENERGY_OUTPUT_FILE = "energy_output.txt"

    # timestep [yr]
    dt = 0.001

    # actual orbital periods of the planets in Earth years (for comparison)
    REAL_PERIODS = {
        "sun": 0.0, # the sun doesn't orbit anything, it just stays at the center
        "mercury": 0.2408467,
        "venus": 0.61519726,
        "earth": 1.0000174,
        "mars": 1.8808476,
        "jupiter": 11.862615,
    }

    # choosing an appropriate threshold angle for planet alignment detection (e.g. 5°)
    phi = float(input("Enter threshold angle (deg) e.g. 5° : "))
    # choosing the total time of the simulation (e.g. 25 years)
    # this has to be done because planet alignment is rare and it might not be detected if the simulation runtime is too short
    TOTAL_TIME = float(input("Enter total simulation time (yr) e.g. 25 yrs : "))

    # loading the class to simulate all the planets (and the sun too)
    sim = simulation.NBodySimulation("parameters_solar.json")

    # creating empty lists for the position histories of the bodies
    positions_history = {body.name: [] for body in sim.bodies}

    # total energy for the system list
    energy_history = []
    # every-10-timesteps for the system list
    time_history = []

    # calculate the total number of steps for this simulation
    steps = int(TOTAL_TIME / dt)
    # after each step,
    for _ in range(steps):
        # do the simulation
        sim.step()
        # for each body in the bodies list,
        for body in sim.bodies:
            # putting xₜ into the list of position histories
            positions_history[body.name].append(body.position.copy())
        # locally storing total energy every 10 steps for plotting a nice graph
        energy_history.append(sim.total_energy())
        # locally storing the time every 10 steps
        time_history.append(sim.time)
        # detecting alignments of planets 
        sim.detect_alignment(threshold_deg=phi)