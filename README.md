---

## Files

---

### Names of files

- simulation.py
- experiment_1.py
- experiment_2.py
- experiment_4.py
- energy_output.txt
- parameters_solar.json
- parse_json.py

---

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

---

### parse_json.py
Sample code for parsing a JSON file holding planet information. The printing is for illustration only and does not need to be included in your own project code. Masses are in units of the Earth mass ($M_{\oplus}$), and orbital radii are in units of the Earth's value (i.e., 1 Astronomical Unit or AU).

---

### experiment_1.py
Upon running this file, the user is asked to pick a value for $dt$ which is basically the update ammount for time in each timestep.
Each timestep follows an update rule ( $t' = t + dt$ )
Depending on the choice of timestep, the orbits of the planets could be more or less accurate than the true value of the orbits.
A timestep too small or too large could potentially accumulate more error during the simulation. So a perfectly right timestep must be picked.
The default timestep for the simulation in **simulation.py** was $dt = 0.001[\text{yr}]$.

After Entering the timestep, the program simulates the orbital periods of all the 5 planets and checks them against their true orbital periods.
The actual values of the orbital periods of the planets can be found here : https://solarsystem.nasa.gov/planet-compare/
After checking the simulated periods against the actual periods, the program computes the **percentage error** (for each planet) and displays it in a tabular format.

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
