# pylint: disable=invalid-name
from enum import Enum

from maya_mock.base import MockedSession


class EnumTypes(Enum):
    Transform = 1
    Shape = 2
    Utility = 3  # (dg)


class MockedCmdsSession(object):
    """
    Mock for the `maya.cmds` module
    """

    def __init__(self, session=None):
        """
        :param MockedSession session: The mocked session for this adaptor.
        """
        if session is None:
            session = MockedSession()
        self._session = session

    @property
    def session(self):
        """
        :return: The interface session
        :rtype: MockedSession
        """
        return self._session

    def _conform_connection_ports(self, src, dst):
        port_src = self.session.get_port_by_match(src)
        if port_src is None:
            raise RuntimeError('The source attribute %r cannot be found.' % src)

        port_dst = self.session.get_port_by_match(dst)
        if port_dst is None:
            raise RuntimeError('The destination attribute %r cannot be found.' % dst)

        return port_src, port_dst

    def _handle_unimplemented_kwargs(self, kwargs):
        if kwargs:
            raise NotImplementedError("Not implemented keyword argument%s: %s" % (
                's' if len(kwargs) else '',
                ', '.join(kwargs.keys())
            ))

    def addAttr(self, *objects, **kwargs):
        """
        Create an attribute

        See `documentation <https://download.autodesk.com/us/maya/2009help/CommandsPython/addAttr.html>`__ for details.

        """
        # Retrieve the attribute name.
        name_long = kwargs.get('longName')
        name_short = kwargs.get('shortName')
        if not name_long and not name_short:
            raise RuntimeError("New attribute needs either a long (-ln) or short (-sn) attribute name.")

        default = kwargs.get('defaultValue', 0.0)

        name = name_long or name_short

        port_type = (
                kwargs.get('attributeType') or
                kwargs.get('at') or
                kwargs.get('dataType') or
                kwargs.get('dt') or
                'float'
        )

        for object_ in objects:
            node = self.session.get_node_by_match(object_)
            self.session.create_port(node, name, port_type=port_type, short_name=name_short, value=default)

    def allNodeTypes(self, **kwargs):
        """
        List known node types.

        See `documentation <https://download.autodesk.com/us/maya/2011help/CommandsPython/allNodeTypes.html>`__ for details.
        """
        raise NotImplementedError

    def createNode(self, _type, name=None, parent=None, shared=None, skipSelect=None):
        """
        Create a node

        See `documentation <https://knowledge.autodesk.com/search-result/caas/CloudHelp/cloudhelp/2018/ENU/Maya-Tech-Docs/CommandsPython/createNode-html.html>`__ for details.
        """
        parent = self.session.get_node_by_match(parent) if parent else None
        node = self.session.create_node(_type, name=name, parent=parent)
        name = node.__melobject__()

        # Select the new node except if -skipSelect
        if not skipSelect:
            self.select([name])

        return name

    def connectionInfo(self, dagpath, sourceFromDestination=False, destinationFromSource=False):
        """
        Get information about connection sources and destinations.

        See `documentation <https://help.autodesk.com/cloudhelp/2017/ENU/Maya-Tech-Docs/Commands/connectionInfo.html>`__ for details.

        :param str dagpath: A port dag path
        :param bool sourceFromDestination:
        :param bool destinationFromSource:
        :return: A boolean when asking for a property, depending on the flags used.
           A string when asking for a plug name.
           A string list When asking for a list of plugs.
        :rtype: bool or str or list(str)
        """
        port = self.session.get_port_by_match(dagpath)
        if sourceFromDestination and not destinationFromSource:
            return next(
                (connection.src.__melobject__() for connection in self.session.get_port_input_connections(port)), ''
            )
        elif destinationFromSource and not sourceFromDestination:
            return [connection.dst.__melobject__() for connection in self.session.get_port_output_connections(port)]
        elif sourceFromDestination and destinationFromSource:
            raise RuntimeError('You cannot specify more than one flag.')
        else:  # elif not sourceFromDestination and not destinationFromSource
            raise RuntimeError('You must specify exactly one flag.')

    def connectAttr(self, src, dst, **kwargs):
        """
        Create a connection

        See `documentation <https://help.autodesk.com/cloudhelp/2016/ENU/Maya-Tech-Docs/CommandsPython/connectAttr.html>`__ for details.

        :param str src: The connection source port.
        :param str dst: The connection destination port.
        """
        self._handle_unimplemented_kwargs(kwargs)
        src, dst = self._conform_connection_ports(src, dst)

        for connection in self.session.connections:
            if connection.src is src and connection.dst is dst:
                # This also raise this warning to the script editor:
                self.warning('%r is already connected to %r.' % (src, dst))
                raise RuntimeError('Maya command error')

        self.session.create_connection(src, dst)

    def delete(self, name, **kwargs):
        """
        Delete nodes

        See `documentation <https://download.autodesk.com/us/maya/2009help/CommandsPython/delete.html>`__ for details.

        :param str name: A pattern defining what to delete.
        :param kwargs: Any additional keyword argument is not implemented.
        """
        node = self.session.get_node_by_name(name)
        self.session.remove_node(node)

    def disconnectAttr(self, src, dst, **kwargs):
        """
        Delete a connection

        See `documentation <http://download.autodesk.com/us/maya/2009help/CommandsPython/disconnectAttr.html>`__ for details.

        :param str src: The connection source port.
        :param str dst: The connection destination port.
        :param kwargs: Any additional keyword argument is not implemented.
        """
        self._handle_unimplemented_kwargs(kwargs)
        src, dst = self._conform_connection_ports(src, dst)
        connection = self.session.get_connection_by_ports(src, dst)

        if not connection:
            raise RuntimeError(u"There is no connection from '{}' to '{}' to disconnect".format(
                src.__melobject__(), dst.__melobject__(),
            ))

        self.session.remove_connection(connection)

    def deleteAttr(self, *queries, **kwargs):
        """
        Delete an attribute (port).

        See `documentation <https://download.autodesk.com/us/maya/2010help/CommandsPython/deleteAttr.html>`__ for details.
        """
        attribute = kwargs.get('attribute') or kwargs.get('at')

        for query in queries:
            # If the provided value match a specific port, delete it.
            port = self.session.get_port_by_match(query)
            if port:
                self.session.remove_port(port)
                continue

            query = '.'.join((query, attribute))
            port = self.session.get_port_by_match(query)
            self.session.remove_port(port)

    def getAttr(self, dagpath):
        """
        Get the value associated with an attribute.

        See `documentation <https://download.autodesk.com/us/maya/2009help/CommandsPython/getAttr.html>`__ for details.1

        :param str dagpath: A dagpath to an attribute.
        :return: The value associated with that attribute.
        :rtype: bool
        """
        port = self.session.get_port_by_match(dagpath)
        if port is None:
            raise ValueError('No object matches name: %s' % dagpath)
        return port.value

    def listAttr(self, *objects, **kwargs):
        """
        List node attributes (ports).

        See `documentation <https://help.autodesk.com/cloudhelp/2017/ENU/Maya-Tech-Docs/Commands/listAttr.html>`__ for details.
        """
        userDefined = kwargs.pop('userDefined', False)

        self._handle_unimplemented_kwargs(kwargs)

        def _filter_port(port):
            if userDefined and not port.user_defined:
                return False
            return True

        nodes = {node for object_ in objects for node in self.session.get_nodes_by_match(object_)}
        ports = (port for node in nodes for port in self.session.ports_by_node.get(node, {}))
        ports = filter(_filter_port, ports)
        return [port.name for port in ports]

    def ls(self, pattern=None, long=False, selection=False, type=None):  # TODO: Verify symbol name?
        """
        List nodes

        See `documentation <https://download.autodesk.com/us/maya/2011help/Commands/ls.html>`__ for details.

        :param str pattern: The pattern to match
        :param bool long: If True, return dag paths
        :param bool selection: If True, return selection
        :param bool type: If set, return only nodes of this type
        :return: A list of node
        :rtype: list of str
        """

        def _filter(node):
            """
            Determine if a node can be yield.
            :param MockedNode n: The node to check.
            :return: True if the node can be yield, False otherwise.
            :rtype: bool
            """
            if selection and node not in self.session.selection:
                return False
            if type and node.type != type:
                return False
            return True

        def _get(n):
            if long:
                return n.dagpath
            else:
                return n.__melobject__()

        nodes = [node for node in self.session.iter_node_by_match(pattern) if _filter(node)]
        return [_get(node) for node in sorted(nodes)]

    def nodeType(self, name):
        """
        Query a node type

        See `documentation <https://help.autodesk.com/cloudhelp/2018/ENU/Maya-Tech-Docs/Commands/nodeType.html>`__ for details.

        :return: The type of the node.
        :rtype: bool
        """
        node = self.session.get_node_by_name(name)
        return node.type

    def objExists(self, pattern):
        """
        Determine if an object exist.

        See `documentation <https://download.autodesk.com/us/maya/2009help/CommandsPython/objExists.html>`__ for details.

        :param str pattern: The pattern to check.
        :return: True if an existing object match the provided pattern, False otherwise.
        :rtype: bool
        """
        return self.session.node_exist(pattern) or bool(self.session.get_port_by_match(pattern))

    def select(self, names):
        """
        Select nodes in the scene that match a specific pattern.

        See `documentation <https://download.autodesk.com/us/maya/2010help/CommandsPython/select.html>`__ for details.

        :param str names: A list of node names to select.
        """

        def _find_node(node):
            for n in self.session.nodes:
                if n.name in names:
                    yield n

        self.session.selection = [y for name in names for y in _find_node(name)]

    def setAttr(self, dagpath, value):
        """
        Set the value of an attribute.

        See `documentation <https://download.autodesk.com/global/docs/maya2012/en_us/CommandsPython/setAttr.html>`__ for details.

        :param str dagpath: The dagpath to an attribute.
        :param object value: The new value of the attribute.
        """
        port = self.session.get_port_by_match(dagpath)
        port.value = value

    def parent(self, *dag_objects, **kwargs):
        """
        Parent nodes

        See `documentation <https://download.autodesk.com/global/docs/maya2012/en_us/CommandsPython/parent.html>`__ for details

        :param dag_objects: The objects to parent.
        :param bool world: Will unparent provided objects if True.
        :param kwargs: Any other keyword arguments are not implemented.
        """
        world = kwargs.pop('world', False)

        self._handle_unimplemented_kwargs(kwargs)

        if world:
            children = dag_objects
            parent = None
        else:
            children = dag_objects[:-1]
            parent = dag_objects[-1]

        # Convert to our internal datatype
        children = [self.session.get_node_by_name(child) for child in children]
        parent = self.session.get_node_by_name(parent)

        for child in children:
            child.set_parent(parent)

    def warning(self, msg):
        """
        Log a warning to stdout.

        See `documentation <https://download.autodesk.com/global/docs/maya2014/en_us/CommandsPython/warning.html>`__ for details.

        :param str msg: The message to log
        """
        self.session.warning(msg)
