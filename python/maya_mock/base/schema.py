import logging

LOG = logging.getLogger(__name__)


class NodeTypeDef(object):
    def __init__(self, node_type, data, classification):
        """
        :param str node_type: The name of the node type (ex: 'transform')
        :param dict(str, dict) data: A dict(k,v) where:
        - k is a standard a port name for this type
        - v is a dict containing the necessary information to build this port
        :param tuple(str) classification: The classification of the type as returned by cmds.getClassification.
        """
        self.type = node_type
        self.data = data
        self.classification = classification

    def apply(self, session, node):
        """
        Create the ports on a provided mocked node.

        :param maya_mock.MockedSession session: The mocked session.
        :param maya_mock.MockedNode node: The node to add ports to.
        """
        for port_name, port_data in self.data.iteritems():
            session.create_port(node, port_name, user_defined=False, **port_data)

    def to_dict(self):
        """
        :return: A serialization python dict version of this instance.
        :rtype: dict
        """
        return {
            'node_type': self.type,
            'attributes': self.data,
            'classification': self.classification
        }

    @classmethod
    def from_dict(cls, data):
        """

        :param dict data:
        :return:
        """
        node_type = data['node_type']
        attributes = data['attributes']
        classification = data['classification']
        return cls(node_type, attributes, classification)

    @classmethod
    def generate(cls, node_type):
        """
        Retreive information about a registered node type in Maya as a dict.

        :param str node_type: The type of node to inspect.
        :return: An object dict
        :rtype: dict
        """
        from maya_mock.base import _maya

        data = _maya.get_node_attributes_info(node_type)
        classification = _maya.get_node_classification(node_type)

        return cls(node_type, data, classification)


class MockedSessionSchema(object):
    """
    Hold information about known nodes and their ports.
    """

    def __init__(self, nodes=None, default_state=None):
        """
        :param nodes: An optional dict(k,v) for registered nodes where:
        - k is the name of the node type
        - v is the node type definition.
        :type nodes: dict(str, NodeTypeDef) or None
        :param default_state: An optional dict(k,v) for default nodes in an empty scene where:
        - k is the name of the node
        - v is the type of the node
        :type default_state: dict(str, str) or None
        """
        if nodes and not isinstance(nodes, dict):
            raise ValueError("Cannot initialize a schema from %s: %r" % (type(nodes), nodes))
        self.nodes = nodes or {}
        self.default_state = default_state or {}

    def register_node(self, node):
        """
        :param NodeTypeDef node: The node type to register.
        """
        if node.type in self.nodes:
            raise Exception("Node type %r is already registered!" % node.type)

        self.nodes[node.type] = node

    def get(self, node_type):  # TODO: rethink
        return self.nodes.get(node_type)

    def get_known_node_types(self):
        """
        :return: All the known node types.
        :rtype: list[str]
        """
        return self.nodes.keys()

    @classmethod
    def generate(cls, fn_progress=None):
        """
        Generate a Schema instance by analysing the current session.

        :return: A new Schema instance
        :rtype: MockedSessionSchema
        """
        from maya import cmds

        # Determine empty scene default state
        cmds.file(new=True, force=True)
        default_state = {name: cmds.nodeType(name) for name in cmds.ls()}

        inst = cls(default_state=default_state)

        # Determine known nodes and their ports
        node_types = cmds.allNodeTypes(includeAbstract=False)
        num_types = len(node_types)

        for i, node_type in enumerate(node_types):

            if fn_progress:
                fn_progress(i, num_types, node_type)

            # TODO: Mark abstract node types as abstract so they can't be created in a mocked session
            # node_type2 = node_type.rstrip(' (abstract)')
            # parent_type = cmds.nodeType(node_type, isTypeName=True, inherited=True)

            try:
                node_def = NodeTypeDef.generate(node_type)
            except RuntimeError as e:  # This happen on HIKCharacterStateClien?
                LOG.warning("Failed to generate NodeTypeDef for %r: %s", node_type, e)
                continue

            if node_def:
                inst.register_node(node_def)

        return inst

    # Serialization methods

    def to_dict(self):
        return {
            'nodes': {node_type: node_def.to_dict() for node_type, node_def in self.nodes.iteritems()},
            'default_state': self.default_state,
        }

    @classmethod
    def from_dict(cls, data):
        """
        Load a Schema from a raw dict.

        :param dict data: A dict, generally obtained from a JSON file.
        :return: A new Schema instance
        :rtype: MockedSessionSchema
        """
        nodes = data.get('nodes') or {}
        default_state = data.get('default_state') or {}

        nodes = {node_name: NodeTypeDef.from_dict(node_data) for node_name, node_data in nodes.iteritems()}

        inst = cls(
            nodes=nodes,
            default_state=default_state
        )

        return inst

    @classmethod
    def from_json_file(cls, path):
        """
        Load a Schema from a json file.

        :param str path: The absolute path to a json file.
        :return: A new MockedSessionSchema instance
        :rtype: MockedSessionSchema
        """
        import json

        with open(path) as fp:
            data = json.load(fp)

        return cls.from_dict(data)

    def to_json_file(self, path, indent=1, sort_keys=True, **kwargs):
        import json

        data = self.to_dict()
        with open(path, "w") as fp:
            json.dump(data, fp, sort_keys=sort_keys, indent=indent, **kwargs)
