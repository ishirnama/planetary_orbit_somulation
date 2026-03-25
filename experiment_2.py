import simulation
import matplotlib.pyplot as plt
import numpy as np

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

    # choosing integration method
    meth = input("Choose an integration method from the following :\n1. Beeman\n2. Euler-Cromer\n3. Direct Euler\n\nEnter the number corresponding to your chosen method : ")

    # loading the class to simulate all the planets (and the sun too)
    sim = simulation.NBodySimulation("parameters_solar.json", meth)

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
    
    names = {
        "1" : "Beeman",
        "2" : "Euler-Cromer",
        "3" : "Direct-Euler"
    }

    # showing the total energy evolution of the system overtime on a graph
    N = len(time_history)
    # plotting ΣE(t) vs t and making sure the units are there
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    t = np.array(time_history)
    E = np.array(energy_history)
    # finding the average total energy of the system
    E_mean = np.mean(E)
    # finding the RMS error of the total energy of the system compared to it's average total energy
    rms = np.sqrt(np.mean((E - E_mean)**2))

    # plotting ΣE(t) vs t
    ax1.plot(t, E*(10**6), color=sim.colour, label=fr"Total Energy ({names[sim.method]}) $\Sigma E(t)$")
    ax1.set_xlabel("t [yr]")
    ax1.set_ylabel(r"$\Sigma E(t)$ [$1\times10^{-6} M_\oplus AU^2 yr^{-2}$]")
    ax1.set_title(f"Total Energy vs Time ({names[sim.method]})")
    ax1.legend()
    ax1.ticklabel_format(style='plain', axis='y')
    # plotting RMS vs t
    ax2.axhline(rms*(10**6), linestyle='--', label=r"$\Delta E_{\mathrm{RMS}}$")
    ax2.set_xlabel("t [yr]")
    ax2.set_ylabel(r"$\Delta E_{\mathrm{RMS}}$ [$1\times10^{-6} M_\oplus AU^2 yr^{-2}$]")
    ax2.set_title("RMS Energy Deviation")
    ax2.legend()
    plt.tight_layout()
    plt.show()