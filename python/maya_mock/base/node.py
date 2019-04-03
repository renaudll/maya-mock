"""A mocked node"""
from maya_mock.base import naming
from maya_mock.base.constants import SHAPE_CLASS


class MockedNode(object):
    """
    A mocked Maya node
    """

    def __init__(self, session, node_type, name, parent=None):
        """
        :param maya_mock.MockedSession session: The parent session.
        :param str node_type: The type associated with the node (ex: 'transform').
        :param str name: The name of the node.
        :param parent: The parent of the node if applicable.
        :type parent: MockedNode or None
        """
        super(MockedNode, self).__init__()

        # Ensure name is unicode as in Maya
        if type(name) is str:
            name = unicode(name)

        self._session = session
        self.name = name
        self.type = node_type
        self._parent = None
        self.ports = set()  # internal REGISTRY_DEFAULT of ports associated with the node
        self.children = set()

        if parent:
            self.set_parent(parent)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __ne__(self, other):
        return hash(self) != hash(other)

    def __gt__(self, other):
        return self.dagpath > other.dagapth

    def __lt__(self, other):
        return self.dagpath < other.dagpath

    def __ge__(self, other):
        return self.dagpath >= other.dagpath

    def __le__(self, other):
        return self.dagpath <= other.dagpath

    def __hash__(self):
        # Note: We can't use the dagpath as the hash source since it can change.
        # This might prevent us from accessing a MockedNode that was stored in a dict
        # before it was re-parented.
        return super(MockedNode, self).__hash__()

    def __repr__(self):
        return '<Mocked Node "{}">'.format(self.dagpath)

    def __melobject__(self):
        """
        Return the node mel representation.
        If multiple nodes exists with the same name, the dagpath will be returned instead.

        :return: The node name or dagpath.
        :rtype: str
        """
        session = self._session
        pattern = self.name
        node = self

        # Precise the pattern until there's no ambiguity remaining
        while session.is_pattern_clashing(self, pattern):
            parent = node.parent
            if parent:
                pattern = naming.join(parent.name, pattern)
                node = parent
            else:
                pattern = '|' + pattern
                break

        return pattern

    @property
    def dagpath(self):
        """
        In Maya, the dagpath is the unique identifier for the resource.
        Return the fully qualified dagpath.
        """
        prefix = self._parent.dagpath + '|' if self._parent else "|"
        return "{}{}".format(prefix, self.name)

    @property
    def parent(self):
        """
        :return: The parent of the node.
        :rtype: maya_mock.MockedNode
        """
        return self._parent

    def set_parent(self, parent):
        """
        Change the node parent.
        :param maya_mock.MockedNode parent: The new parent to set.
        """
        if self._parent:
            self._parent.children.discard(self)  # TODO: .remove instead of discard?
        if parent:
            parent.children.add(self)
        self._parent = parent

    def get_port_by_name(self, name):  # TODO: Deprecate? This should be called from session instead
        """
        Query a specific node port by it's name.
        :param str name: The name of the port to search.
        :return: A Port if a match is found. Return None otherwise.
        :rtype: maya_mock.MockedPort or None
        """
        for port in self.ports:
            if port.name == name:
                return port
        return None

    def isShape(self):
        """
        Determine if the current node instance if a shape.

        :return: True if the node is a shape, False otherwise.
        :rtype: bool
        """
        return self.type in SHAPE_CLASS
