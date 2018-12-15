

class MockedPymelNode(object):
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
        session = self.__session
        port = session.get_node_port_by_name(self._node, name)
        return port.value

    def hasAttr(self, name):
        session = self.__session
        return session.get_node_port_by_name(self._node, name) is not None

    def name(self):
        return self._node.name

    def nodeName(self):
        return self._node.name

    def fullPath(self):
        return self._node.dagpath

    def getParent(self):
        pymel = self.__pymel
        parent = self._node.parent
        if parent is None:
            return None
        return pymel._node_to_pynode(parent)

    def setParent(self, *args, **kwargs):
        pymel = self.__pymel
        pymel.parent(self, *args, **kwargs)

    def getChildren(self):
        session = self.__session
        pymel = self.__pymel
        parent = self._node
        # TODO: Does ordering matter?
        return [pymel._node_to_pynode(node) for node in session.nodes if node.parent is parent]
