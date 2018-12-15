import pytest


def test_createNode(cmds):
    """ Validate result when calling createNode without any name."""
    cmds.createNode('transform')
    assert cmds.objExists('transform1')


def test_createNode_multi(cmds):
    """ Validate result when calling createNode multiple times without any name."""
    cmds.createNode('transform')
    cmds.createNode('transform')
    assert cmds.objExists('transform1')
    assert cmds.objExists('transform2')


def test_createNode_name(cmds):
    """ Validate result when calling createNode and specifying a name that don't exist."""
    cmds.createNode("transform", name="foo")
    assert cmds.objExists('foo')


def test_createNode_name_multi(cmds):
    """ Validate result when calling createNode and specifying a name that exist."""
    cmds.createNode("transform", name="foo")
    cmds.createNode("transform", name="foo")
    cmds.createNode("transform", name="foo")
    assert cmds.objExists('foo')
    assert cmds.objExists('foo1')
    assert cmds.objExists('foo2')


def test_delete(cmds):
    """ Validate that we can delete a node using the `delete` function."""
    cmds.createNode("transform")
    cmds.delete("transform1")
    assert not cmds.objExists("transform1")


def test_selection_empty_by_defaut(cmds):
    """ Validate that we the selection is empty by default."""
    assert cmds.ls(selection=True) == []


def test_selection_on_node_creationg(cmds):
    """ Validate that when a node is created it is automatically selected."""
    cmds.createNode("transform", name="foo")
    assert cmds.ls(selection=True) == ['foo']


def test_createNode_skipSelect(cmds):
    """Validate that when creating node using the `skipSelect` kwarg, the selected don't change."""
    cmds.createNode("transform", name='a')
    cmds.createNode("transform", name='b', skipSelect=True)
    assert cmds.ls(selection=True) == ['a']


def test_select_clear(cmds):
    """ Ensure we are able to clear a selection."""
    cmds.createNode('transform')
    cmds.select([])
    assert cmds.ls(selection=True) == []


def test_select(cmds):
    """ Ensure we are able to select a node."""
    cmds.createNode('transform')
    cmds.select([])
    cmds.select(['transform1'])
    assert cmds.ls(selection=True) == ['transform1']


def test_addAttr(cmds):
    """Ensure we can create a port."""
    node = cmds.createNode('transform')
    cmds.addAttr(node, longName='foo')

    assert cmds.objExists('transform1.foo')


def test_addAttr_missingName(cmds):
    """Ensure a RuntimeError is raised when trying to use addAttr without the `longName` or `shortName` flag."""
    node = cmds.createNode('transform')
    with pytest.raises(RuntimeError) as exception:
        cmds.addAttr(node)
    # TODO: Use absolute comparison, there's an issue with the last '\n' character.
    # assert exception.match(u'New attribute needs either a long (-ln) or short (-sn) attribute name.')


def test_getAttr_defaultValue(cmds):
    """Ensure we can query the value of a port."""
    node = cmds.createNode('transform')
    cmds.addAttr(node, longName='foo', defaultValue=1.0)
    assert cmds.getAttr('transform1.foo') == 1


def test_setAttr(cmds):
    """Ensure we can change the value of a port."""
    node = cmds.createNode('transform')
    cmds.addAttr(node, longName='foo')
    cmds.setAttr('transform1.foo', 20)
    assert cmds.getAttr('transform1.foo') == 20


def test_connectAttr(cmds):
    """Ensure we can create a connection."""
    node = cmds.createNode('transform')
    cmds.addAttr(node, longName='src')
    cmds.addAttr(node, longName='dst')
    cmds.connectAttr('transform1.src', 'transform1.dst')

    assert cmds.connectionInfo('transform1.src', destinationFromSource=True) == ['transform1.dst']
    assert cmds.connectionInfo('transform1.src', sourceFromDestination=True) == ''
    assert cmds.connectionInfo('transform1.dst', sourceFromDestination=True) == 'transform1.src'
    assert cmds.connectionInfo('transform1.dst', destinationFromSource=True) == []


def test_connectAttr_existing_connection(cmds):
    """Ensure that trying to create a connection using already connection nodes raise a RuntimeError."""
    node = cmds.createNode('transform')
    cmds.addAttr(node, longName='src')
    cmds.addAttr(node, longName='dst')
    cmds.connectAttr('transform1.src', 'transform1.dst')
    with pytest.raises(RuntimeError) as exception:
        cmds.connectAttr('transform1.src', 'transform1.dst')
    assert str(exception.value) == 'Maya command error'


@pytest.fixture
def connection(cmds):
    node = cmds.createNode('transform')
    cmds.addAttr(node, longName='src')
    cmds.addAttr(node, longName='dst')
    cmds.connectAttr('transform1.src', 'transform1.dst')


@pytest.mark.usefixtures('connection')
def test_disconnectAttr(cmds):
    """Ensure that trying to create a connection using already connection nodes raise a RuntimeError."""
    cmds.disconnectAttr('transform1.src', 'transform1.dst')
    assert cmds.connectionInfo('transform1.src', destinationFromSource=True) == []
    assert cmds.connectionInfo('transform1.src', sourceFromDestination=True) == ''
    assert cmds.connectionInfo('transform1.dst', sourceFromDestination=True) == ''
    assert cmds.connectionInfo('transform1.dst', destinationFromSource=True) == []


@pytest.mark.usefixtures('connection')
def test_disconnectAttr_no_connection(cmds):
    with pytest.raises(RuntimeError) as exception:
        cmds.disconnectAttr('transform1.dst', 'transform1.src')  # note: args are inverted
    # TODO: Use absolute comparison, there's an issue with the last '\n' character.
    assert exception.match(ur"There is no connection from 'transform1.dst' to 'transform1.src' to disconnect")
