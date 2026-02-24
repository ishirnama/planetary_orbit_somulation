"""
Sample code for parsing a JSON file holding planet information. The
printing is for illustration only and does not need to be included in
your own project code. Masses are in units of the Earth mass, and
orbital radii are in units of the Earth's value (i.e., 1 Astronomical
Unit or AU).
"""

import json

if __name__ == "__main__":
    with open("parameters_solar.json") as f:
        parameters_solar = json.load(f)

    for body in parameters_solar["bodies"]:
        print(f"{body['name']} has mass {body['mass']}, orbital radius "
              f"{body['orbital_radius']}, and colour {body['colour']}")
