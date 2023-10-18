"""
Brody Soedel
Provides tests for KSP App
"""

import orbital_velocity as ov
import math


def orbital_velocity_tests():
    test_value = ov.velocity(5.2915158e22, 80_000, 600_000)
    expected = 2279
    assert math.isclose(test_value, expected, rel_tol=1), \
        str(test_value) + " != " + str(expected)


def main():
    orbital_velocity_tests()


if __name__ == "__main__":
    main()
