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


def test_selection_empty_by_defaut(cmds):
    """ Validate that we the selection is empty by default."""
    assert cmds.ls(selection=True) == []


def test_selection_on_node_creationg(cmds):
    """ Validate that when a node is created it is automatically selected."""
    cmds.createNode("transform", name="foo")
    assert cmds.ls(selection=True) == ['foo']


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
