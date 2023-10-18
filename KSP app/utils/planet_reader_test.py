"""
Brody Soedel
tests for planet_reader.py
"""

import planet_reader
import math


def mass_test():
    """
    tests mass calculation of mass_from_g
    """
    test_planets = planet_reader.PlanetReader("testfiles")
    print(test_planets.mass_from_g(1, 600_000))
    assert \
        math.isclose(
            5.2915158e+22,
            test_planets.mass_from_g(1, 600_000), rel_tol=1e-4
            )


def main():
    mass_test()


if __name__ == "__main__":
    main()
