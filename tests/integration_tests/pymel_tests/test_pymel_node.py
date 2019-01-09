# coding: utf-8
"""
Unit-tests for maya_mock pymel implementation.
"""
import pytest


@pytest.fixture
def node(pymel):
    """Fixture for a node with a single attribute."""
    node = pymel.createNode('transform')
    pymel.addAttr(node, longName='foo')
    return node


def test_node_name(node):
    """Validate the `name` method behavior"""
    actual = node.name()
    assert actual == 'transform1'
    assert type(actual) is unicode


def test_node_fullPath(node):
    """Validate the `fullPath` method behavior"""
    assert node.fullPath() == '|transform1'


def test_node_nodeName(node):
    """Validate the `nodeName` method behavior"""
    assert node.nodeName() == 'transform1'


def test_node__melobject__(node):
    """Validate the `__melobject__` magic method behavior"""
    actual = node.__melobject__()
    assert actual == 'transform1'
    assert type(actual) is unicode


def test__melobject_clash(session, pymel):
    """Validate that when calling __melobject__ on a node with a non-unique name, it's dagpath is returned."""
    parent = session.create_node('transform')
    child = session.create_node('transform', parent=parent)
    assert parent.__melobject__() == '|transform1'
    assert child.__melobject__() == 'transform1|transform1'


def test_node__str__(node):
    """Validate the `__str__` magic method behavior."""
    actual = str(node)
    assert actual == 'transform1'
    assert type(actual) is str


def test_node__repr__(node):
    """Validate the `__repr__` magic method behavior."""
    actual = repr(node)
    assert actual == "nt.Transform(u'transform1')"
    assert type(actual) is str


def test_node__getattr__(pymel, node):
    """Validate we can access attribute via the __getattr__ magic method."""
    port = node.foo
    assert type(port) is pymel.Attribute
    assert port.longName() == 'foo'


def test_node__getattr__missing(node):
    """Validate a RuntimeError is raised if trying to access a missing attribute via the __getattr__ magic method."""
    with pytest.raises(AttributeError):
        node.fooMissing
    # assert str(exception.value) == ''  # TODO: Validate exception message


def test_node_attr(pymel, node):
    """Validate the `attr` method behavior"""
    port = node.attr('foo')
    assert type(port) is pymel.Attribute


def test_node_getAttr(node):
    """Validate the `getAttr` method behavior"""
    assert node.getAttr('foo') == 0.0


def test_node_hasAttr(node):
    """Validate the `hasAttr` method behavior"""
    assert node.hasAttr('foo')


def test_node_setParent(pymel):
    """Validate the `setParent` method behavior"""
    parent = pymel.createNode("transform", name="parent")
    child = pymel.createNode("transform", name="child")

    child.setParent(parent)
    assert child.getParent() == parent

    child.setParent(world=True)
    assert child.getParent() is None


def test_node_getChildren(pymel):
    """Validate the `getChildren` method behavior"""
    parent = pymel.createNode("transform", name="parent")
    child = pymel.createNode("transform", name="child")
    child.setParent(parent)
    assert parent.getChildren() == [child]
