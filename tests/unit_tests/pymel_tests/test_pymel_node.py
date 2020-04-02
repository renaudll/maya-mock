"""
Test cases for MockedPymelNode
"""
# pylint: disable=redefined-outer-name
import six

import pytest


@pytest.fixture
def node(pymel):
    """Fixture for a node with a single attribute."""
    node = pymel.createNode("transform")
    pymel.addAttr(node, longName="foo")
    return node


def test_name(node):
    """Validate the `name` method behavior"""
    actual = node.name()
    assert actual == "transform1"
    assert isinstance(actual, six.text_type)


def test_fullPath(node):  # pylint: disable=invalid-name
    """Validate the `fullPath` method behavior"""
    assert node.fullPath() == "|transform1"


def test_nodeName(node):  # pylint: disable=invalid-name
    """Validate the `nodeName` method behavior"""
    assert node.nodeName() == "transform1"


def test__melobject__(node):
    """Validate the `__melobject__` magic method behavior"""
    actual = node.__melobject__()
    assert actual == "transform1"
    assert isinstance(actual, six.text_type)


def test__str__(node):
    """Validate the `__str__` magic method behavior."""
    actual = str(node)
    assert actual == "transform1"
    assert isinstance(actual, str)


def test__repr__(node):
    """Validate the `__repr__` magic method behavior."""
    actual = repr(node)
    assert actual == "nt.Transform(u'transform1')"
    assert isinstance(actual, str)


def test__getattr__(pymel, node):
    """Validate we can access attribute via the __getattr__ magic method."""
    port = node.foo
    assert isinstance(port, pymel.Attribute)
    assert port.longName() == "foo"


def test__getattr__missing(node):
    """
    Validate a RuntimeError is raised if trying to access
    a missing attribute via the __getattr__ magic method.
    """
    with pytest.raises(AttributeError):
        _ = node.fooMissing
    # assert str(exception.value) == ''  # TODO: Validate exception message


def test_attr(pymel, node):
    """Validate the `attr` method behavior"""
    port = node.attr("foo")
    assert isinstance(port, pymel.Attribute)


def test_getAttr(node):  # pylint: disable=invalid-name
    """Validate the `getAttr` method behavior"""
    assert node.getAttr("foo") == 0.0


def test_hasAttr(node):  # pylint: disable=invalid-name
    """Validate the `hasAttr` method behavior"""
    assert node.hasAttr("foo")


def test_setParent(pymel):  # pylint: disable=invalid-name
    """Validate the `setParent` method behavior"""
    parent = pymel.createNode("transform", name="parent")
    child = pymel.createNode("transform", name="child")

    child.setParent(parent)
    assert child.getParent() == parent

    child.setParent(world=True)
    assert child.getParent() is None


def test_getChildren(pymel):  # pylint: disable=invalid-name
    """Validate the `getChildren` method behavior"""
    parent = pymel.createNode("transform", name="parent")
    child = pymel.createNode("transform", name="child")
    child.setParent(parent)
    assert parent.getChildren() == [child]
