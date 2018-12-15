from maya import cmds


class NodeTypeDef(object):
    def __init__(self, node_type, data):
        self.type = node_type
        self.data = data

    def apply(self, session, node):
        """
        Create the ports on a provided mocked node.

        :param maya_mock.MockedSession session: The mocked session.
        :param maya_mock.MockedNode node: The node to add ports to.
        """
        for port_name, port_data in self.data.iteritems():
            session.create_port(node, port_name, **port_data)

    @classmethod
    def generate(cls, node_type):
        data = {}

        attributes = cmds.attributeInfo(allAttributes=True, type=node_type)
        for attribute in attributes:
            attr_type = cmds.attributeQuery(attribute, type=node_type, attributeType=True)

            # Some attributes will return 'typed' as the type.
            # I don't know of any way of knowing in advance the type.
            # However for what we need, guessing might be enough.
            if attr_type == 'typed':
                if 'matrix' in attribute.lower():  # HACK
                    attr_type = 'matrix'

            attr_name_short = cmds.attributeQuery(attribute, type=node_type, shortName=True)
            attr_name_nice = cmds.attributeQuery(attribute, type=node_type, niceName=True)

            attr_data = {
                'port_type': attr_type,
                'short_name': attr_name_short,
                'nice_name': attr_name_nice,
            }

            data[attribute] = attr_data

        return cls(node_type, data)


class SessionSchema(object):
    """
    Hold information about known nodes and their ports.
    """

    def __init__(self):
        self.data = {}

    def register_node(self, node):
        """
        :param NodeTypeDef node: The node type to register.
        """
        if node.type in self.data:
            raise Exception("Node type %r is already registered!" % node.type)

        self.data[node.type] = node

    def get(self, node_type):  # TODO: rethink
        return self.data.get(node_type)

    @classmethod
    def generate(cls):
        """
        Generate a Schema instance by analysing the current session.

        :return: A new Schema instance
        :rtype: SessionSchema
        """
        inst = cls()

        node_types = cmds.allNodeTypes(includeAbstract=False)
        for node_type in node_types:
            node_def = NodeTypeDef.generate(node_type)
            if node_def:
                inst.register_node(node_def)

        return inst
