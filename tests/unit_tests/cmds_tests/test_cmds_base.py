"""
Test cases for MockedCmdsSession
Theses test should not depend on any specific schema.
"""
import pytest


# TODO: test_createNode_shape
# TODO: test createNode_shape_twiceWithSameName
# TODO: test_partial_dagpath (ex: ['transform1|a', 'transform2|b'])


def test_createNode(cmds):  # pylint: disable=invalid-name
    """ Validate result when calling createNode without any name."""
    cmds.createNode("transform")
    assert cmds.objExists("transform1")


def test_createNode_multi(cmds):  # pylint: disable=invalid-name
    """ Validate result when calling createNode multiple times without any name."""
    cmds.createNode("transform")
    cmds.createNode("transform")
    assert cmds.objExists("transform1")
    assert cmds.objExists("transform2")


def test_createNode_name(cmds):  # pylint: disable=invalid-name
    """ Validate result when calling createNode and specifying a name that don't exist."""
    cmds.createNode("transform", name="foo")
    assert cmds.objExists("foo")


def test_createNode_name_multi(cmds):  # pylint: disable=invalid-name
    """ Validate result when calling createNode and specifying a name that exist."""
    cmds.createNode("transform", name="foo")
    cmds.createNode("transform", name="foo")
    cmds.createNode("transform", name="foo")
    assert cmds.objExists("foo")
    assert cmds.objExists("foo1")
    assert cmds.objExists("foo2")


def test_createNode_name_with_namespace(cmds):  # pylint: disable=invalid-name
    """ Validate result when calling createNode and using a name with a namespace."""
    result = cmds.createNode("transform", name="foo:bar")
    assert result == u"foo:bar"
    assert cmds.objExists("foo:bar")


def test_delete(cmds):
    """ Validate that we can delete a node using the `delete` function."""
    cmds.createNode("transform")
    cmds.delete("transform1")
    assert not cmds.objExists("transform1")


def test_ls_name(cmds):
    """ Validate we ca list object matching a name."""
    cmds.createNode("transform", name="transformA")
    assert cmds.ls("transformA") == ["transformA"]


def test_ls_name_pattern(cmds):
    """ Validate we can list object matching provided node name pattern."""
    cmds.createNode("transform", name="transformA")
    actual = cmds.ls("transform*")
    assert actual == [u"transformA"]


def test_ls_order(cmds):
    """ Validate we ls return object in alphabetical order even if it don't match creation order."""
    cmds.createNode("transform", name="transformB")
    cmds.createNode("transform", name="transformA")
    assert cmds.ls("transform*") == ["transformA", "transformB"]


def test_ls_wildcard(cmds):
    """ Validate we can use ls with a wildcard."""
    cmds.createNode("transform", name="foo1")
    cmds.createNode("transform", name="foo2")
    assert cmds.ls("foo*") == ["foo1", "foo2"]


def test_ls_type(cmds):
    """ Validate we can use ls and specify a type."""
    cmds.createNode("transform")
    cmds.createNode("multiplyDivide")
    assert cmds.ls(type="multiplyDivide") == ["multiplyDivide1"]


def test_ls_dag_clashes(cmds):
    """
    Validate that when two node have clashing name and `long` is False,
    we'll get a partial representation.
    """
    cmds.createNode("transform", name="parent")
    cmds.createNode("transform", name="child", parent="parent")
    cmds.createNode("transform", name="child")

    assert cmds.ls("child") == ["|child", "parent|child"]


def test_ls_long_dagnode(cmds):
    """ Validate we can use ls with the `long` kwarg on dagnodes."""
    cmds.createNode("transform")
    assert cmds.ls("transform*", type="transform", long=True) == [u"|transform1"]


@pytest.mark.skip("Not implemented yet")
def test_ls_long_nondagnode(cmds):
    """ Validate we can use ls with the `long` kwarg on non dagnodes."""
    cmds.createNode("network")
    assert cmds.ls("network", type="network", long=True) == [u"network1"]


def test_selection_empty_by_defaut(cmds):
    """ Validate that we the selection is empty by default."""
    assert cmds.ls(selection=True) == []


def test_selection_on_node_creationg(cmds):
    """ Validate that when a node is created it is automatically selected."""
    cmds.createNode("transform", name="foo")
    assert cmds.ls(selection=True) == ["foo"]


def test_createNode_parent(cmds):  # pylint: disable=invalid-name
    """Validate that we can create node using the `parent` kwarg."""
    cmds.createNode("transform", name="transformA")
    cmds.createNode("transform", name="transformB", parent="transformA")
    assert cmds.ls("transform*", type="transform", long=True) == [
        "|transformA",
        "|transformA|transformB",
    ]


def test_createNode_skipSelect(cmds):  # pylint: disable=invalid-name
    """Validate that when creating node using the `skipSelect` kwarg, the selected don't change."""
    cmds.createNode("transform", name="a")
    cmds.createNode("transform", name="b", skipSelect=True)
    assert cmds.ls(selection=True) == ["a"]


def test_select_clear(cmds):
    """ Ensure we are able to clear a selection."""
    cmds.createNode("transform")
    cmds.select([])
    assert cmds.ls(selection=True) == []


def test_select(cmds):
    """ Ensure we are able to select a node."""
    cmds.createNode("transform")
    cmds.select([])
    cmds.select(["transform1"])
    assert cmds.ls(selection=True) == ["transform1"]


def test_addAttr(cmds):  # pylint: disable=invalid-name
    """Ensure we can create a port."""
    node = cmds.createNode("transform")
    cmds.addAttr(node, longName="foo")

    assert cmds.objExists("transform1.foo")


def test_addAttr_missingName(cmds):  # pylint: disable=invalid-name
    """
    Ensure a RuntimeError is raised when trying to use addAttr
    without the `longName` or `shortName` flag.
    """
    node = cmds.createNode("transform")
    with pytest.raises(RuntimeError):
        cmds.addAttr(node)
    # TODO: Use absolute comparison, there's an issue with the last '\n' character.
    # assert exception.match(
    #     u"New attribute needs either a long (-ln) or short (-sn) attribute name."
    # )


def test_deleteAttr(cmds):  # pylint: disable=invalid-name
    """Ensure we can delete a dynamic attribute."""
    node = cmds.createNode("transform")
    cmds.addAttr(node, longName="foo")
    cmds.deleteAttr(node, attribute="foo")
    assert not cmds.objExists("transform1.foo")


def test_getAttr_default_value(cmds):  # pylint: disable=invalid-name
    """Ensure we can namespace the value of a port."""
    node = cmds.createNode("transform")
    cmds.addAttr(node, longName="foo", defaultValue=1.0)
    assert cmds.getAttr("transform1.foo") == 1.0


def test_getAttr_invalid_path(cmds):  # pylint: disable=invalid-name
    """Ensure we fail the same way as Maya when calling getAttr with a non-existent dag path."""
    cmds.createNode("transform")
    with pytest.raises(ValueError) as exception:
        cmds.getAttr("transform1.a_missing_attribute")
    assert exception.match("No object matches name: transform1.a_missing_attribute")


def test_getAttr_shortName(cmds):  # pylint: disable=invalid-name
    """Ensure we can call getAttr using a port short name."""
    node = cmds.createNode("transform")
    cmds.addAttr(node, longName="fooLong", shortName="fooShort", defaultValue=1.0)
    assert cmds.getAttr("transform1.fooShort") == 1.0


def test_getAttr_niceName(cmds):  # pylint: disable=invalid-name
    """Ensure that like Maya, we can't call getAttr from a port using it's nice name."""
    node = cmds.createNode("transform")
    cmds.addAttr(node, longName="fooLong", niceName="fooNice", defaultValue=1.0)
    with pytest.raises(ValueError) as exception:
        cmds.getAttr("transform1.fooNice")
    assert exception.match("No object matches name: transform1.fooNice")


def test_setAttr(cmds):  # pylint: disable=invalid-name
    """Ensure we can change the value of a port."""
    node = cmds.createNode("transform")
    cmds.addAttr(node, longName="foo")
    cmds.setAttr("transform1.foo", 20)
    assert cmds.getAttr("transform1.foo") == 20


def test_listAttr(cmds):  # pylint: disable=invalid-name
    """Ensure listAttr work as expected."""
    node = cmds.createNode("transform")
    cmds.addAttr(node, longName="foo")
    assert cmds.listAttr(node, userDefined=True) == ["foo"]


def test_nodeType(cmds):  # pylint: disable=invalid-name
    """Ensure nodeType work as expected."""
    node = cmds.createNode("transform")
    assert cmds.nodeType(node) == "transform"
