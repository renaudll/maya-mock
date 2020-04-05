"""
Test cases for MockedCmdsSession port related methods
"""
# pylint: disable=redefined-outer-name
import pytest


@pytest.fixture
def node(cmds):
    """Create a "transform1" node"""
    return cmds.createNode("transform")


def test_addAttr(cmds, node):  # pylint: disable=invalid-name
    """Ensure we can create a port."""
    cmds.addAttr(node, longName="foo")

    assert cmds.objExists("transform1.foo")


def test_addAttr_missingName(cmds, node):  # pylint: disable=invalid-name
    """
    Ensure a RuntimeError is raised when trying to use addAttr
    without the `longName` or `shortName` flag.
    """
    with pytest.raises(RuntimeError):
        cmds.addAttr(node)
    # TODO: Use absolute comparison, there's an issue with the last '\n' character.
    # assert exception.match(
    #     u"New attribute needs either a long (-ln) or short (-sn) attribute name."
    # )


def test_deleteAttr(cmds, node):  # pylint: disable=invalid-name
    """Ensure we can delete an attribute."""
    cmds.addAttr(node, longName="foo")
    cmds.deleteAttr(node, attribute="foo")
    assert not cmds.objExists("transform1.foo")


@pytest.mark.usefixtures("node")
def test_deleteAttr_missing_attribute_arg(cmds):  # pylint: disable=invalid-name
    """Ensure we raise if we try to delete an attribute but don't provide it's name."""
    with pytest.raises(RuntimeError) as exception:
        cmds.deleteAttr("transform1")
    assert exception.match("Must specify attribute to be deleted.\n")


def test_deleteAttr_invalid_attribute(cmds, node):  # pylint: disable=invalid-name
    """Ensure we raise if we try to delete an attribute that don't exist."""
    with pytest.raises(RuntimeError) as exception:
        cmds.deleteAttr(node, attribute="foo")
    assert exception.match("Node 'transform1' does not have attribute 'foo'.\n")


def test_deleteAttr_valid_path(cmds, node):  # pylint: disable=invalid-name
    """Ensure we can delete an attribute by it's path."""
    cmds.addAttr(node, longName="foo")
    cmds.deleteAttr("transform1.foo")
    assert not cmds.objExists("transform1.foo")


@pytest.mark.usefixtures("node")
def test_deleteAttr_invalid_path(cmds):  # pylint: disable=invalid-name
    """Ensure we raise if we try to delete an attribute by a missing path."""
    with pytest.raises(ValueError) as exception:
        cmds.deleteAttr("transform1.foo")
    assert exception.match("No object matches name: transform1.foo")


def test_deleteAttr_valid_path_and_invalid_attribute(
    cmds, node
):  # pylint: disable=invalid-name
    """Ensure if we provide an attribute path and an attribute name, the attribute name is used."""
    cmds.addAttr(node, longName="foo")
    with pytest.raises(RuntimeError) as exception:
        cmds.deleteAttr("transform1.foo", attribute="bar")
    assert exception.match("Node 'transform1' does not have attribute 'bar'.")


def test_deleteAttr_invalid_path_and_valid_attribute(
    cmds, node
):  # pylint: disable=invalid-name
    """Ensure we raise if we provide a valid attribute and an invalid path."""
    cmds.addAttr(node, longName="foo")
    with pytest.raises(ValueError) as exception:
        cmds.deleteAttr("transform1.bar", attribute="foo")
    assert exception.match("No object matches name: transform1.bar")


def test_getAttr_default_value(cmds, node):  # pylint: disable=invalid-name
    """Ensure we can namespace the value of a port."""
    cmds.addAttr(node, longName="foo", defaultValue=1.0)
    assert cmds.getAttr("transform1.foo") == 1.0


@pytest.mark.usefixtures("node")
def test_getAttr_invalid_path(cmds):  # pylint: disable=invalid-name
    """Ensure we fail the same way as Maya when calling getAttr with a non-existent dag path."""
    with pytest.raises(ValueError) as exception:
        cmds.getAttr("transform1.a_missing_attribute")
    assert exception.match("No object matches name: transform1.a_missing_attribute")


def test_getAttr_shortName(cmds, node):  # pylint: disable=invalid-name
    """Ensure we can call getAttr using a port short name."""
    cmds.addAttr(node, longName="fooLong", shortName="fooShort", defaultValue=1.0)
    assert cmds.getAttr("transform1.fooShort") == 1.0


def test_getAttr_niceName(cmds, node):  # pylint: disable=invalid-name
    """Ensure that like Maya, we can't call getAttr from a port using it's nice name."""
    cmds.addAttr(node, longName="fooLong", niceName="fooNice", defaultValue=1.0)
    with pytest.raises(ValueError) as exception:
        cmds.getAttr("transform1.fooNice")
    assert exception.match("No object matches name: transform1.fooNice")


def test_setAttr(cmds, node):  # pylint: disable=invalid-name
    """Ensure we can change the value of a port."""
    cmds.addAttr(node, longName="foo")
    cmds.setAttr("transform1.foo", 20)
    assert cmds.getAttr("transform1.foo") == 20


def test_listAttr(cmds, node):  # pylint: disable=invalid-name
    """Ensure listAttr work as expected."""
    cmds.addAttr(node, longName="foo")
    assert cmds.listAttr(node, userDefined=True) == ["foo"]
