

class MockedNode(object):
    """
    A mocked Maya node
    """
    def __init__(self, session, node_type, name):
        super(MockedNode, self).__init__()

        # Ensure name is unicode
        if type(name) is str:
            name = unicode(name)

        self._session = session
        self.name = name
        self.type = node_type
        self._parent = None
        self.ports = set()  # internal REGISTRY_DEFAULT of ports associated with the node
        self.children = set()

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __ne__(self, other):
        return hash(self) != hash(other)

    # Note: We can't use the dagpath as the hash source since it can change.
    # This might prevent us from accessing a MockedNode that was stored in a dict
    # before it was re-parented.
    # def __hash__(self):
    #     return hash(self.dagpath)

    def __repr__(self):
        return '<Mocked Node "{}">'.format(self.dagpath)

    def __melobject__(self):
        """ Return the node name.

        If multiple nodes exists with the same name, the dagpath will be returned instead.
        :param MockedNode node: The node to query
        :return: The node name.
        :rtype: str
        """
        registry = self._session
        if any(True for node in registry.nodes if node != self and node.name == self.name):
            return self.dagpath
        return self.name

    def match(self, pattern):
        """
        Check if the node match a certain pattern.
        The pattern can be a fully qualified dagpath or a name.

        - "child"
        - "child*"
        - "|child"

        :param pattern:
        :return:
        """
        # HACK: Poor-man pattern matching...
        # TODO: Make more solid
        if not pattern:
            return True
        return pattern in self.dagpath

    @property
    def dagpath(self):
        """
        In Maya, the dagpath is the unique identifier for the resource.
        Return the fully qualified dagpath.
        """
        prefix = self._parent.dagpath if self._parent else "|"
        return "{}{}".format(prefix, self.name)

    @property
    def parent(self):
        return self._parent

    def set_parent(self, parent):
        if self._parent:
            self._parent.children.discard(self)  # TODO: .remove instead of discard?
        if parent:
            parent.children.add(self)
        self._parent = parent

    def get_port_by_name(self, name):
        for port in self.ports:
            if port.name == name:
                return port
        return None
