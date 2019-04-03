"""Mock for pymel.core.PyNode"""


# pylint: disable=invalid-name


class MockedPymelNode(object):
    """
    A pymel.core.PyNode mock.

    Original documentation:
    https://help.autodesk.com/cloudhelp/2018/CHS/Maya-Tech-Docs/PyMel/generated/classes/pymel.core.general/pymel.core.general.PyNode.html#pymel.core.general.PyNode
    """
    def __init__(self, pymel, node):
        self.__pymel = pymel
        self.__session = pymel.session
        self._node = node
        self.selected = False

    def __str__(self):
        return self.__melobject__()

    def __repr__(self):
        return "nt.%s(%r)" % (self._node.type.title(), self._node.name)

    def __getattr__(self, item):
        """
        pymel behavior when __getattr__ is called is to try to resolve a port with the name.
        :param str item: The attribute name.
        :return:
        :raise: AttributeError: If no port if found matching the name.
        """
        session = self.__session
        pymel = self.__pymel

        port = session.get_node_port_by_name(self._node, item)
        if port:
            mock = pymel._port_to_attribute(port)
            return mock

        raise AttributeError("{} has no attribute or method named '{}'".format(self, item))

    def __melobject__(self):
        return self._node.__melobject__()

    def attr(self, name):
        session = self.__session
        pymel = self.__pymel

        port = session.get_node_port_by_name(self._node, name)
        return pymel._port_to_attribute(port)

    def getAttr(self, name):
        """
        Query the value of an attribute.

        :param str name: The dagpath of an attribute.
        :return: The value of the attribute.
        :rtype: bool
        """
        session = self.__session
        port = session.get_node_port_by_name(self._node, name)
        return port.value

    def hasAttr(self, name, checkShape=True):
        """
        Convenience function for determining if an object has an attribute.
        If checkShape is enabled, the shape node of a transform will also be checked for the attribute.

        :param str name: The name of the attribute to check.
        :param bool checkShape: Determine if we also need to check the shape of the node is a transform. Default is True.
        :return: True if the object has the provided attribute. False otherwise.
        :rtype:bool
        """
        session = self.__session

        # If the node is a tranform and checkShape is True, also check it's shape.
        if self._node.type == 'transform' and checkShape:
            for shape in self.getShapes():
                if session.get_node_port_by_name(shape, name):
                    return True

        return session.get_node_port_by_name(self._node, name) is not None

    def name(self):
        """
        :return: The name of the node.
        :rtype:str
        """
        return self._node.name

    def nodeName(self):
        """
        :return: Just the name of the node, without any dag path.
        :rtype: str
        """
        return self._node.name

    def fullPath(self):
        """
        :return: The full dag path to the object, including leading pipe (|).
        :rtype: str
        """
        return self._node.dagpath

    def getParent(self, generation=1):
        """
        Return the parent of this node.

        :param int generation: Gives the number of levels up that you wish to go for the parent.
        :return: The parent node or None if node have no parent.
        :rtype: MockedPymelNode or None
        """
        pymel = self.__pymel
        node = self._node
        for i in range(generation):
            node = node.parent

        return pymel._node_to_pynode(node) if node else None

    def setParent(self, *args, **kwargs):
        """
        Reparent the current node.

        :param tuple args: Any positional argument are sent to `cmds.setParent`.
        :param dict kwargs: Any keyword arguments are sent to `cmds.setParent`.
        """
        pymel = self.__pymel
        pymel.parent(self, *args, **kwargs)

    def getChildren(self):
        """
        Query the children of this node.

        :return: A list of nodes
        :rtype: list(MockedPymelNode)
        """
        session = self.__session
        pymel = self.__pymel
        parent = self._node
        # TODO: Does ordering matter?
        return [pymel._node_to_pynode(node) for node in session.nodes if node.parent is parent]

    def getShapes(self):
        """
        Query the shapes of this node.
        This only work on transform node.

        :return: A list of nodes.
        :rtype: list(MockedPymelNode)
        """
        session = self.__session
        pymel = self.__pymel
        parent = self._node
        nodes = [node for node in session.nodes if node.parent is parent and session and node.isShape()]
        return [pymel._node_to_pynode(node) for node in nodes]
