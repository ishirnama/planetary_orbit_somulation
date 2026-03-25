----------------------------------------
## Files
----------------------------------------

### Names of files

- simulation.py
- experiment_1.py
- experiment_2.py
- experiment_4.py

### Simulation
simulation.py contains 2 classes :
- Body
- NBodySimulation

The Body class is a template for each planet. It contains **all the details** about the planets and the information given about them in the JSON file **(parameters_solar.json)**.
For example, some of the attributes of the Body class include :
- name (name of the planet)
- mass (mass of the planet in units of $M_\oplus$ "Earth Mass")
- colour (colour of the planet used in the simulation)
- position (position of the planet in the solar system $r(t)$ in units of $AU$ "Astronomical Units")

Upon running simulation.py , the program calculates the position vectors $r(t)$ for each planet at each timestep.
Then, an animation pops up showing the planets moving around the sun (according to their positions for each timestep calculated earlier).
Each timestep is 0.001 of a year and the program calculates the simulation for 25 years (since that's how long it takes for jupiter to complete 2 orbits around the sun).

---

### parameters_solar.json
Contains initial conditions for the solar system bodies.

s.py
Runs the default simulation and produces an animation of planetary orbits.

run_experiment1.py
Computes orbital periods of planets and compares them with real values.

run_experiment2.py
Compares energy conservation for different numerical integration methods:
- Beeman
- Euler-Cromer
- Direct Euler

run_experiment4.py
Detects planetary alignments based on a 5° threshold from the mean angle.

----------------------------------------
## How to run the files
----------------------------------------

Make sure you have Python installed with the following libraries:
- numpy
- matplotlib
- json (standard)

To run a file:

python run_default.py
python run_experiment1.py
python run_experiment2.py
python run_experiment4.py

----------------------------------------
## Units used for calculations
----------------------------------------

- Distance: AU
- Mass: Earth masses (M⊕)
- Time: years
