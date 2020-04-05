"""
Mocks for a `maya.cmds` session
"""
# TODO: Implement cmds.allNodeTypes
from maya_mock.base import MockedSession
from maya_mock.base._utils import handle_arguments, redirect_method_args_to_arg


class MockedCmdsSession(object):
    """
    Mock for the `maya.cmds` module
    """

    def __init__(self, session=None):
        """
        :param MockedSession session: The mocked session for this adaptor.
        """
        self._session = session or MockedSession()

    @property
    def session(self):
        """
        :return: The interface session
        :rtype: MockedSession
        """
        return self._session

    def _conform_connection_ports(self, src, dst):
        try:
            port_src = self.session.get_port_by_match(src)
        except LookupError:
            raise RuntimeError("The source attribute %r cannot be found." % src)

        try:
            port_dst = self.session.get_port_by_match(dst)
        except LookupError:
            raise RuntimeError("The destination attribute %r cannot be found." % dst)

        return port_src, port_dst

    @redirect_method_args_to_arg
    @handle_arguments(
        attributeType="at",
        dataType="dt",
        defaultValue="dv",
        longName="ln",
        niceName="nn",
        shortName="sn",
    )  # pylint: disable=invalid-name,too-many-arguments
    def addAttr(
        self,
        objects,
        attributeType=None,
        dataType=None,
        defaultValue=0.0,
        longName=None,
        niceName=None,
        shortName=None,
    ):  # pylint: disable: invalid-name,too-many-arguments
        """
        Create an attribute

        https://download.autodesk.com/us/maya/2009help/CommandsPython/addAttr.html

        :param str attributeType: The attribute type
        :param str dataType: The attribute data type
        :param object defaultValue: The attribute default value
        :param str longName: The attribute long name
        :param str shortName: The attribute short name
        :param tuple[str] objects: Objects to add the attribute to
        """
        # Retrieve the attribute name.
        if not longName and not shortName:
            raise RuntimeError(
                "New attribute needs either a long (-ln) or short (-sn) attribute name."
            )

        name = longName or shortName
        port_type = attributeType or dataType or "float"

        for object_ in objects:
            node = self.session.get_node_by_match(object_)
            self.session.create_port(
                node,
                name,
                port_type=port_type,
                short_name=shortName,
                value=defaultValue,
                nice_name=niceName,
            )

    @handle_arguments(name="n", parent="p", skipSelect="ss")
    def createNode(
        self, type_, name=None, parent=None, skipSelect=False
    ):  # pylint: disable=invalid-name
        """
        Create a node

        https://knowledge.autodesk.com/search-result/caas/CloudHelp/cloudhelp/2018/ENU/Maya-Tech-Docs/CommandsPython/createNode-html.html

        :param str type_: A node type
        :param str name: A node name
        :parent str parent: An optional node parent
        :param bool skipSelect: If True, the node creation won't affect the current selection.
        """
        parent = self.session.get_node_by_match(parent) if parent else None
        node = self.session.create_node(type_, name=name, parent=parent)
        name = node.__melobject__()

        # Select the new node except if -skipSelect
        if not skipSelect:
            self.select([name])

        return name

    @handle_arguments(sourceFromDestination="sdf", destinationFromSource="dfs")
    def connectionInfo(
        self, dagpath, sourceFromDestination=False, destinationFromSource=False
    ):  # pylint: disable=invalid-name
        """
        Get information about connection sources and destinations.

        https://help.autodesk.com/cloudhelp/2017/ENU/Maya-Tech-Docs/Commands/connectionInfo.html

        :param str dagpath: A port dag path
        :param bool sourceFromDestination:
        :param bool destinationFromSource:
        :return: A boolean when asking for a property, depending on the flags used.
           A string when asking for a plug name.
           A string list When asking for a list of plugs.
        :rtype: bool or str or list(str)
        """
        try:
            port = self.session.get_port_by_match(dagpath)
        except LookupError:
            raise ValueError("No object matches name: %s" % dagpath)

        if sourceFromDestination and not destinationFromSource:
            return next(
                (
                    connection.src.__melobject__()
                    for connection in self.session.get_port_input_connections(port)
                ),
                "",
            )

        if destinationFromSource and not sourceFromDestination:
            return [
                connection.dst.__melobject__()
                for connection in self.session.get_port_output_connections(port)
            ]

        if sourceFromDestination and destinationFromSource:
            raise RuntimeError("You cannot specify more than one flag.")

        raise RuntimeError("You must specify exactly one flag.")

    @handle_arguments(force="f")
    def connectAttr(self, src, dst, force=False):  # pylint: disable=invalid-name
        """
        Create a connection

        https://help.autodesk.com/cloudhelp/2016/ENU/Maya-Tech-Docs/CommandsPython/connectAttr.html

        :param str src: The connection source port.
        :param str dst: The connection destination port.
        :param bool force: If the destination is already connected, the old connection is broken.
        """
        src, dst = self._conform_connection_ports(src, dst)

        connection = next(iter(self.session.get_port_input_connections(dst)), None)
        if connection:
            if force:
                self.session.remove_connection(connection)
            else:
                # This also raise this warning to the script editor:
                self.warning("%r is already connected to %r." % (src, dst))
                raise RuntimeError("Maya command error")

        self.session.create_connection(src, dst)
        # TODO: Simplify
        return u"Connected %s.%s to %s.%s." % (
            src.node.name,
            src.name,
            dst.node.name,
            dst.name,
        )

    @handle_arguments()
    def delete(self, name):
        """
        Delete nodes

        https://download.autodesk.com/us/maya/2009help/CommandsPython/delete.html

        :param str name: A pattern defining what to delete.
        """
        # TODO: What happen if the node don't exit?
        node = self.session.get_node_by_name(name)
        self.session.remove_node(node)

    @handle_arguments()
    def disconnectAttr(self, src, dst):  # pylint: disable=invalid-name
        """
        Delete a connection

        http://download.autodesk.com/us/maya/2009help/CommandsPython/disconnectAttr.html

        :param str src: The connection source port.
        :param str dst: The connection destination port.
        """
        src, dst = self._conform_connection_ports(src, dst)
        connection = self.session.get_connection_by_ports(src, dst)

        if not connection:
            raise RuntimeError(
                u"There is no connection from '{}' to '{}' to disconnect".format(
                    src.__melobject__(), dst.__melobject__(),
                )
            )

        self.session.remove_connection(connection)

    @handle_arguments(attribute="at")
    def deleteAttr(self, node, attribute=None):  # pylint: disable=invalid-name
        """
        Delete an attribute (port).

        https://download.autodesk.com/us/maya/2010help/CommandsPython/deleteAttr.html

        :param str: A node name of an attribute path
        :param str: An attribute name
        :raises RuntimeError: If the attribute was not found.
        """
        # Backup the original asked name, we need to re-use it in error message.
        query = node

        # In all case, maya will raise a ValueError if the node or path don't exist.
        try:
            node = self.session.get_node_by_name(node)
        except LookupError:
            try:
                node = self.session.get_port_by_match(node).node
            except LookupError:
                raise ValueError("No object matches name: %s" % node)

        if attribute is None:
            try:
                port = self.session.get_port_by_match(query)
            except LookupError:
                raise RuntimeError("Must specify attribute to be deleted.\n")
        else:
            try:
                port = self.session.get_node_port_by_name(node, attribute)
            except LookupError:
                raise RuntimeError(
                    "Node %r does not have attribute %r.\n"
                    % (str(node.name), attribute)
                )

        self.session.remove_port(port)

    @handle_arguments()
    def getAttr(self, dagpath):  # pylint: disable=invalid-name
        """
        Get the value associated with an attribute.

        https://download.autodesk.com/us/maya/2009help/CommandsPython/getAttr.html

        :param str dagpath: A dagpath to an attribute.
        :return: The value associated with that attribute.
        :rtype: bool
        """
        try:
            port = self.session.get_port_by_match(dagpath)
        except LookupError:
            raise ValueError("No object matches name: %s" % dagpath)
        return port.value

    @redirect_method_args_to_arg
    @handle_arguments(userDefined="ud")
    def listAttr(self, objects, userDefined=False):  # pylint: disable=invalid-name
        """
        List node attributes (ports).

        https://help.autodesk.com/cloudhelp/2017/ENU/Maya-Tech-Docs/Commands/listAttr.html

        :param tuple[str] objects: Objects to list attributes from
        :return: A list of attribute names
        :rtype: list[str]
        """

        def _filter_port(port):
            if userDefined and not port.user_defined:
                return False
            return True

        nodes = {
            node
            for object_ in objects
            for node in self.session.get_nodes_by_match(object_)
        }
        ports = (
            port for node in nodes for port in self.session.ports_by_node.get(node, {})
        )
        ports = filter(_filter_port, ports)
        return [port.name for port in ports]

    @redirect_method_args_to_arg
    @handle_arguments(long="l", selection="sl", type="typ")
    def ls(
        self, objects, long=False, selection=False, type=None
    ):  # pylint: disable=invalid-name,redefined-builtin
        """
        List nodes

        https://download.autodesk.com/us/maya/2011help/Commands/ls.html

        :param bool long: If True, return dag paths
        :param bool selection: If True, return selection
        :param bool type: If set, return only nodes of this type
        :param tuple[str] objects: The pattern to match
        :return: A list of node
        :rtype: list of str
        """
        pattern = next(iter(objects), None)
        # TODO: Support multiple objects

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
            return n.__melobject__()

        nodes = [
            node for node in self.session.iter_node_by_match(pattern) if _filter(node)
        ]
        return [_get(node) for node in sorted(nodes)]

    @handle_arguments()
    def nodeType(self, name):  # pylint: disable=invalid-name
        """
        Query a node type

        https://help.autodesk.com/cloudhelp/2018/ENU/Maya-Tech-Docs/Commands/nodeType.html

        :return: The type of the node.
        :rtype: bool
        """
        # TODO: What happen if the node don't exist?
        node = self.session.get_node_by_name(name)
        return node.type

    def objExists(self, pattern):  # pylint: disable=invalid-name
        """
        Determine if an object exist.

        https://download.autodesk.com/us/maya/2009help/CommandsPython/objExists.html

        :param str pattern: The pattern to check.
        :return: True if an existing object match the provided pattern, False otherwise.
        :rtype: bool
        """
        try:
            self.session.get_port_by_match(pattern)
        except LookupError:
            pass
        else:
            return True

        return self.session.node_exist(pattern)

    @handle_arguments()
    def select(self, names):
        """
        Select nodes in the scene that match a specific pattern.

        https://download.autodesk.com/us/maya/2010help/CommandsPython/select.html

        :param list[str] names: A list of node names to select.
        """
        # TODO: Implement pattern matching
        self.session.selection = [
            node for node in self.session.nodes if node.name in names
        ]

    @handle_arguments()
    def setAttr(self, dagpath, value):  # pylint: disable=invalid-name
        """
        Set the value of an attribute.

        https://download.autodesk.com/global/docs/maya2012/en_us/CommandsPython/setAttr.html

        :param str dagpath: The dagpath to an attribute.
        :param object value: The new value of the attribute.
        """
        # TODO: What happen if port is not found?
        port = self.session.get_port_by_match(dagpath)
        port.value = value

    @redirect_method_args_to_arg
    @handle_arguments(world="w")
    def parent(self, objects, world=False):
        """
        Parent nodes

        https://download.autodesk.com/global/docs/maya2012/en_us/CommandsPython/parent.html

        :param objects: The objects to parent.
        :param bool world: Will unparent provided objects if True.
        """
        if world:
            children = objects
            parent = None
        else:
            children = objects[:-1]
            parent = objects[-1]

        # Convert to our internal datatype
        # TODO: What happen if the parent or children don't exist?
        children = [self.session.get_node_by_name(child) for child in children]
        parent = self.session.get_node_by_name(parent) if parent is not None else None

        for child in children:
            child.set_parent(parent)

    @handle_arguments()
    def warning(self, msg, **_):
        """
        Log a warning to stdout.

        https://download.autodesk.com/global/docs/maya2014/en_us/CommandsPython/warning.html

        :param str msg: The message to _LOG
        """
        self.session.warning(msg)
