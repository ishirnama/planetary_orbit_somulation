# Computer Simulation Final Project : PONS (Planetary Orbit Numerical Simulation)
/
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

---

### experiment2.py
Upon runninng this file, the program prompts the user for which integration method they wish to use.
The user can pick from 3 options andd enter the number corresponding to their desired integration method :
1. Beeman
2. Euler-Cromer
3. Direct Euler

Then, the program plots 2 graphs :
- "**Total Energy**" ($E(t)$) against "**time**" ($t$)
- "**Total Energy RMS**" ($\Delta E_{\text{RMS}}$) against "**time**" ($t$)

These graphs help to visualise energy conservation. The first graph displays $\Sigma E(t)$ vs $t$.
From this graph, we can look for properties of energy conservation, i.e. if the energy is bounded (kept within a certain range) then it is conserved.
The second graph ($\Delta E_{\text{RMS}}$ vs $t$) shows how far away the system's total energy ($\Sigma E(t)$) is from the equillibrium ($\braket{E}$).
If $\Delta E_{\text{RMS}}$

---

### experiment4.py
Upon running this file, the program prompts the user for the length of time (yrs) they want to simulate.
Then it asks them for a **threshold angle** ($\phi$). This angle is the maximum possible angle that the position vectors of all the planets can make with a line.
This guarentees a **planetary alignment**. The planetary alignment times are then printed out into the terminal.

---

## How to run the files

Make sure you have Python installed with the following libraries :
- numpy
- matplotlib
- json (standard)

To run a file :

1. Open a terminal
2. Navigate to your project folder.
3. Type "python [filename].py" into the terminal and replace [filename] with the actual file's name (e.g. python simulation.py)
4. Follow the instructions that pop up in the terminal.

---

## Units used for calculations

- Distance : $AU$
- Mass : Earth masses ($M_\oplus$)
- Time : $yr$
