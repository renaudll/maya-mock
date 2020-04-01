"""Mocked for the pymel package."""
from maya_mock.cmds.session import MockedCmdsSession
from maya_mock.pymel.node import MockedPymelNode
from maya_mock.pymel.port import MockedPymelPort


class MockedPymelSession(MockedCmdsSession):
    """
    Mock for the maya.cmds python module

    :param maya_mock.MockedSession session: The mocked session for this adaptor.
    """

    def __init__(self, session):
        super(MockedPymelSession, self).__init__(session)

        self.session.onNodeAdded.connect(self.__callback_node_added)
        self.session.onNodeRemoved.connect(self.__callback_node_removed)
        self.session.onPortAdded.connect(self.__callback_port_added)
        self.session.onPortRemoved.connect(self.__callback_port_removed)

        self._registry = {}

        # pymel.core.PyNode
        self.PyNode = MockedPymelNode

        # pymel.core.Attribute
        self.Attribute = MockedPymelPort

        # Register all existing node
        for node in session.nodes:
            self.__callback_node_added(node)

        # Register all existing port
        for port in session.ports:
            self.__callback_port_added(port)

    def __callback_node_added(self, node):
        """
        Called when a node is added in the scene.
        :param MockedNode node: The node added
        """
        mock = MockedPymelNode(self, node)
        self._registry[node] = mock

    def __callback_node_removed(self, node):
        """
        Called when a node is removed from the scene.
        :param MockedNode node: The node being removed.
        """
        self._registry.pop(node, None)

    def __callback_port_added(self, port):
        mock = MockedPymelPort(self.session, port)
        self._registry[port] = mock

    def __callback_port_removed(self, port):
        self._registry.pop(port, None)

    def _str_to_pynode(self, val):
        """
        Convert a string to a registered MockedPymelNode instance.

        :param str val: A node name or dagpath.
        :return: A MockedPymelNode
        :rtype: MockedPymelNode
        """
        assert isinstance(val, basestring)
        node = self.session.get_node_by_match(val)
        if not node:
            return None
        return self._node_to_pynode(node)

    def _node_to_pynode(self, node):
        """
        Get a MockedPymelNode from an MockedNode instance.

        :param MockedNode node: A mocked node
        :return: A registered MockedPymelNode instance.
        :rtype: MockedPymelNode
        :raise KeyError: If the provided MockedNode is not registered.
        """
        return self._registry[node]

    def _port_to_attribute(self, port):
        """
        Get a MockedPymelPort from a MockedPort instance.
        :param port:
        :return:
        """
        return self._registry[port]

    def _to_mel(self, data):
        """
        Convert a MockedPymelNode to a fully qualified dagpath.

        :param MockedPymelNode data: A PyNode-like object.
        :return: A fully qualified dagpath.
        :rtype: str
        """
        try:
            return data.__melobject__()
        except AttributeError:
            return data

    def ls(self, *args, **kwargs):
        nodes = super(MockedPymelSession, self).ls(*args, **kwargs)
        return [self._str_to_pynode(node) for node in nodes]

    def objExists(self, args):
        names = [str(arg) for arg in args]
        return self.session.node_exist(names)

    def createNode(self, *args, **kwargs):
        node = super(MockedPymelSession, self).createNode(*args, **kwargs)
        return self._str_to_pynode(node)

    def listAttr(self, objects):
        attrs = super(MockedPymelSession, self).listAttr(objects)
        return [MockedPymelPort(self, attr) for attr in attrs]

    def addAttr(self, *objects, **kwargs):
        objects = [self._to_mel(object) for object in objects]
        super(MockedPymelSession, self).addAttr(*objects, **kwargs)

    def select(self, names):
        super(MockedPymelSession, self).select(names)
        return self.ls(selection=True)

    def parent(self, *dagnodes, **kwargs):
        names = [self._to_mel(node) for node in dagnodes]
        super(MockedPymelSession, self).parent(*names, **kwargs)

    def connectAttr(self, src, dst, **kwargs):
        src = self._to_mel(src)
        dst = self._to_mel(dst)
        super(MockedPymelSession, self).connectAttr(src, dst, **kwargs)

    def disconnectAttr(self, src, dst, **kwargs):
        src = self._to_mel(src)
        dst = self._to_mel(dst)
        super(MockedPymelSession, self).disconnectAttr(src, dst, **kwargs)