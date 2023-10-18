"""
Brody Soedel
Program that reads in .cfg files that are used by KSP to store information
"""


class Node:
    """
    A class that represents a node on a .cfg tree
    --------------------------------------------

    Attributes:
        name : str
            name of the node
        params : dict{Param : list}
            a dictionary of the parameters belonging to the node along with a
            map to their values
        nodes: list[Node]
            list of children nodes belonging to that node
        parent_node: Node
            parent node class of current node

    Methods:
        get_name()
            returns the name
        add_param(param)
            adds a Param object to params
        add_node(node)
            adds a Node object to the end of nodes
        get_nodes()
            returns nodes
        get_params()
            returns params
        get_parent_node()
            returns parent_node
        str_recursion(node, indent, return_string)
            recursive method for __str__
        __str__
            formats Node with all subnodes and params in a format that
            represents a file directory
        __repr__
            shows Node with number of subnodes and params
    """
    def __init__(self, name, parent_node):
        """
        Constructs necessary attributes
        ------------------------------
        Parameters:
            name : str
                name of node
            parent_node: Node
                Node that current instance is the child of
        """
        self.name = name
        self.params = {}
        self.nodes = []
        self.parent_node = parent_node

    def get_name(self) -> str:
        """
        Retrieves name of node
        ----------------------
        Returns:
            str
                name of Node
        """
        return self.name

    def add_param(self, param):
        """
        Adds Param object and its value to params
        -------------------------------------------
        Parameters:
            param : Param
                Param object that is to be added
        """
        self.params[param] = param.get_value()

    def add_node(self, node):
        """
        Adds Node object to nodes
        -----------------------
        Parameters:
            node : Node
                Node that is to be added as a subnode
        """
        self.nodes.append(node)

    def get_nodes(self) -> list:
        """
        Retrieves list of child nodes
        -----------------------------
        Returns:
            list[Nodes]
                list of child nodes
        """
        return self.nodes

    def get_params(self) -> dict:
        """
        Retrieves dictionary of Param objects and values attached to node
        -----------------------------------------------------------------
        Returns:
            dict{Param: list}
                Dictioanry containing dict keys of Param objects and dict
                values of a list of the values assigned to parameter
        """
        return self.params

    def get_parent_node(self) -> "Node":
        """
        Retrieves parent node that current node is a child of
        -----------------------------------------------------
        Returns:
            Node
                parent node
        """
        return self.parent_node

    def str_recursion(self, node, indent, return_string) -> str:
        """
        Helper recursion method for __str__, adding a node and parameters
        to __str__ with each recursion
        -----------------------------------
        Parameters:
            node : Node
                current node that is being recursed
            indent : str
                string that is the current indentation being applied to current
                node in __str__ representation in the format of "  |-" , with
                "  |" added before with each recursion depth
            return_string : str
                string that is being passed through to recursion function that
                is being added to

        Returns:
            str
                current __str__ string plus current recursion depth's additions
        """
        return_string += "\n" + indent + node.get_name()
        # TODO refactor into param
        for param in node.get_params():
            return_string += "\n  |" + indent + param.get_name() + \
                " = " + str(param.get_value())
        subnodes = node.get_nodes()
        if len(subnodes) > 0:
            for subnode in subnodes:
                return_string = str(self.str_recursion(subnode, "  |" + indent,
                                    return_string))
            return return_string
        else:
            return return_string

    def __str__(self):
        """
        Returns string representation of node in following format:
          |-self
          |  |-param name = param value
          |  |-param name = param value
          |  |-child
          |  |  |-param name = param value
        ---------------------------------------------------------
        Returns:
            str
                in above format
        """
        return self.str_recursion(self, "  |-", "")

    def __repr__(self):
        """
        Returns more compact representation of nodes for iterables
        ----------------------------------------------------------
        Returns:
            str
                in format: [self :: Nodes: #children;Parameters: #params]
        """
        return self.name + " :: Nodes:" + str(len(self.nodes)) + \
            ";Parameters:" + str(len(self.params))


# Maybe refactor to make just strings and lists instead?
class Param():
    """
    Class that represents parameter in a .cfg tree
    ---------------------------------------------
    Attributes:
        name : str
            name of parameter
        values : list
            list of values attributed to parameter on line in .cfg file

    Methods:
        get_value()
            retrieves values
        get_name()
            retrieves name
    """
    def __init__(self, name, values):
        """
        Initializes object and attributes
        ---------------------------------
        Parameters:
            name : str
                name of parameter
            values : list
                list of values attributed to parameter
        """
        self.name = name
        self.values = values

    def get_value(self) -> list:
        """
        Returns list of values
        ----------------------
        Returns:
            list
                list of values
        """
        return self.values

    def get_name(self) -> str:
        """
        Returns name of parameter
        ------------------------
        Returns:
            str
                name of parameter
        """
        return self.name

    def __str__(self):
        """
        Returns name of parameter as string representation of object
        ------------------------------------------------------------
        Returns:
            str
                name of parameter
        """
        return self.name

    __repr__ = __str__


class Cfg:
    """
        Class that translates and then represents a .cfg file into a series
        of linked object nodes that represent node structure of original file
        --------------------------------------------------------------------
        Attributes:
            name : str
                name of Cfg object retrieved from the name of the cfg file
                with the .cfg ending removed
            nodes : list[Node]
                list of child nodes attached to instance

        Methods:
            add_node(node)
                adds child node to instance
            get_nodes()
                returns the list of child nodes
            get_name()
                returns name of cfg object
    """
    def __init__(self, filename):
        """
        Reads in a provided .cfg file and fills in attributes and object
        structure
        -----------------------------------------------------------------
        Parameters:
            filename : str
                Valid directory path of a .cfg file
        """
        directory = filename.split("\\")
        self.name = directory[-1][:-4]
        self.nodes = []

        with open(filename) as f:
            # gets rid of kopernicus header
            f.readline()
            f.readline()
            current = None
            for line in f:
                line = line.strip()
                line_list = line.split()
                # controls edge cases like comments, starts of nodes,
                # and empty nodes
                try:
                    filter_boolean = line != "{" and line[0] != "!" and \
                        "//" not in line
                # hacky solution probably fix this
                except IndexError:
                    continue
                if filter_boolean:  # TODO probably refactor
                    if line == "}":
                        if (current is not None):
                            current = current.get_parent_node()
                    elif (current is None):
                        new_node = Node(line, None)
                        self.add_node(new_node)
                        current = new_node
                    else:
                        if line != current.name and "=" in line_list:
                            new_param = Param(line_list[0], line_list[2:])
                            current.add_param(new_param)
                        else:
                            new_node = Node(line, current)
                            current.add_node(new_node)
                            current = new_node

    def add_node(self, node):
        """
        Adds a child node to instance
        -----------------------------
        Parameters:
            node : Node
                node to be added
        """
        self.nodes.append(node)

    def get_nodes(self) -> list:
        """
        Returns the list of child nodes of an instance
        ----------------------------------------------
        Returns:
            list[Node]
                list of child nodes
        """
        return self.nodes

    def get_name(self) -> str:
        """
        Returns name of cfg object
        --------------------------
        Returns:
            str
                name of cfg object
        """
        return self.name

    # maybe make this also print like nodes?
    def __str__(self):
        """
        Returns string representation of cfg object
        -------------------------------------------
        Returns:
            str
                in format of name[list of children]
        """
        return self.name + str(self.nodes)

    __repr__ = __str__
