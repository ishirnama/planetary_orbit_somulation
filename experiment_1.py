import simulation

if __name__ == "__main__":

    # simulate 25 years (because Jupiter needs to cross the x-axis at least twice to get an accurate period measurement)
    # once at the start (t = 0)
    # and once at the end (t = 25)
    TOTAL_TIME = 25

    # making a file to store the total energy of the system at each timestep
    ENERGY_OUTPUT_FILE = "energy_output.txt"

    # actual orbital periods of the planets in Earth years (for comparison)
    REAL_PERIODS = {
        "sun": 0.0, # the sun doesn't orbit anything, it just stays at the center
        "mercury": 0.2408467,
        "venus": 0.61519726,
        "earth": 1.0000174,
        "mars": 1.8808476,
        "jupiter": 11.862615,
    }

    # picking a dt value for the simulation to compare accuracy against dt choice
    dt = float(input("Enter a value for the time step (dt) in years (e.g., 0.001): "))

    # loading the class to simulate all the planets (and the sun too)
    sim = simulation.NBodySimulation("parameters_solar.json", dt=dt)

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

    # printing the headers for the orbital period comparison table
    print(f"\n             {'Simulation':<10} | {'Actual':<7} | {'Percentage Error'}")
    # dashed-line to rule off headings from table content
    print("-" * 53)
    # goping through each body,
    for body in sim.bodies:
        # if the body name matches the name of the body in REAL_PERIODS
        if body.name in REAL_PERIODS and body.orbital_period:
            # making a list of the real orbital period values
            real = REAL_PERIODS[body.name]
            # making a list of the simulated orbital period values
            simul = body.orbital_period
            # plugging them into the percentage error formula
            error = abs(simul - real) / real * 100
            # priting the percentage error (simulation vs actual) for each body
            print(f"{body.name:<10} | {simul:<10.3f} | {real:<7.3f} | {error:.2f}% (2 s.f.)")