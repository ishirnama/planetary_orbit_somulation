----------------------------------------
## Files
----------------------------------------

simulation.py
Contains the main simulation code, including:
- Body class
- NBodySimulation class
- Integration methods (Beeman, Euler-Cromer, Euler)

parameters_solar.json
Contains initial conditions for the solar system bodies.

run_default.py
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
