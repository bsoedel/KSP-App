"""
Brody Soedel
Reads in .cfg files of Kopernicus planets and generates a dictionary
containing planets and their planetary characteristics
"""
import cfg_reader
import os
from scipy import constants as c

# looks in config file
# gets geeASL and radius and name
# 9.81g = G(M/r^2)
# (9.81g/G)r^2 = M
# gets mass from this
# creates entry for each name assigning blank dictionary
# dictionary then has mass and radius information added


class PlanetReader:
    """"
    Constructs a dictionary containing the name of a planet with the value
    of a dictionary containing the information of that planet, currently
    mass and radius. Requires the path of the folder containing the Kopernicus
    .cfg files of a given mod to do this.
    -------------------------------------------------------------------------
    Attributes:
        planet_dict : dict
            dictionary containing the keys which are the names of all the
            planetary bodies along with the values which is a dictionary
            containing tuples of planetary characterisics with their values
        directory : str
            filepath of folder containing planet configs

    Methods:
        mass_from_g(geeASL, radius)
            calculates Mass of a planet given the gs at sea level and the
            radius of said planet
        get_directory()
            returns filepath of folder
        get_planet()
            returns constructed planet dictionary containng planetary
            information
    """
    def __init__(self, path):
        """
        Constructs planet dictionary and populates it with each information
        and populates attributes
        -------------------------------------------------------------------
        Parameters:
            path : str
                filepath of folder containing .cfg files
        """
        self.planet_dict = {}
        self.directory = path
        for filename in os.listdir(self.directory):
            planet_file = os.path.join(self.directory, filename)
            if os.path.isfile(planet_file):
                cfg = cfg_reader.Cfg(planet_file)
                planet_name = cfg.get_name()
                self.planet_dict[planet_name] = {}
                planet = self.planet_dict[planet_name]

                # 0 is the index that is where the "Body" node is located
                body_node = cfg.get_nodes()[0]
                for node in body_node.get_nodes():
                    if node.get_name() == "Properties":
                        params = node.get_params()
                        for param, values in params.items():
                            if param.get_name() == "radius":
                                # one value in list
                                planet[param.get_name()] = float(values[0])
                            if param.get_name() == "geeASL":
                                # TODO add mass
                                planet[param.get_name()] = float(values[0])
                planet["mass"] = self.mass_from_g(planet["geeASL"],
                                                  planet["radius"])

    def mass_from_g(self, geeASL, radius) -> float:
        """
        Calculates the Mass of a planet from given gs at sea level as well
        as the radius of that planet
        --------------------------------------------------------------------
        Parameters:
            geeASL : float
                G-Force at sea level
            radius : float
                Radius of planetary body
        Returns:
            float
                Resulting mass calculated from G-Force and radius using
                Newton's law of gravitation
        """
        g_constant = c.G
        mass = ((9.81 * geeASL) / g_constant) * radius ** 2
        return mass

    def get_directory(self) -> str:
        """
        Returns filepath of folder containing .cfg files
        -------------------------------------------------
        Returns:
            str
                filepath of folder
        """
        return self.directory

    def get_planets(self) -> dict:
        """
        Returns planet dictionary containing information
        ------------------------------------------------
        Returns:
            dict
                populated planet dictionary with information on planetary
                characteristics
        """
        return self.planet_dict


# move when actually building app
def main():
    filename = "C:\\JNSQ KSP\\GameData\\JNSQ\\JNSQ_Bodies"
    planet_reader = PlanetReader(filename)
    planets = planet_reader.get_planets()
    print(str(planets))


if __name__ == "__main__":
    main()
