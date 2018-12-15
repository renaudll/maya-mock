# coding: utf-8
"""
Unit-tests for maya_mock pymel implementation.
"""
import pytest


def test_createNode(pymel):
    """
    Validate result when calling createNode without any name.
    The resulting name should have the node type as prefix and a number as suffix.
    """
    node = pymel.createNode('transform')
    assert isinstance(node, pymel.PyNode)
    assert node.name() == 'transform1'


def test_pynode_name(pymel):
    """Ensure we are able to use ``createNode`` and get a valid PyNode is return."""
    # TODO: test clash
    node1 = pymel.createNode('transform')
    assert node1.name() == 'transform1'


def test_pynode_fullPath(pymel):
    """
    Validate PyNode.fullPath behavior.
    """
    node = pymel.createNode('transform')
    assert node.fullPath() == '|transform1'


def test_pynode_nodeName(pymel):
    node = pymel.createNode('transform')
    # TODO: test clash
    assert node.nodeName() == 'transform1'


def test_pynode__getattr__(pymel):
    """Validate we can access attribute via the __getattr__ magic method."""
    node = pymel.createNode('transform')
    pymel.addAttr(node, longName='foo')
    port = node.foo
    assert type(port) is pymel.Attribute
    assert port.longName() == 'foo'


def test_pynode__getattr__missing(pymel):
    """Validate a RuntimeError is raised if trying to access a missing attribute via the __getattr__ magic method."""
    node = pymel.createNode('transform')
    with pytest.raises(AttributeError) as exception:
        node.foo
    # assert str(exception.value) == 'abc'


def test_pynode_attr(pymel):
    """Ensure we can access an attribute via the `getAttr` method."""
    node = pymel.createNode('transform')
    pymel.addAttr(node, longName='foo')
    port = node.attr('foo')
    assert type(port) is pymel.Attribute
    assert port.name() == 'transform1.foo'


def test_pynode_getAttr(pymel):
    node = pymel.createNode('transform')
    pymel.addAttr(node, longName='foo', defaultValue=10.0)
    assert node.getAttr('foo') == 10.0


def test_pynode_hasAttr(pymel):
    node = pymel.createNode('transform')
    pymel.addAttr(node, longName='foo', defaultValue=10.0)
    assert node.hasAttr('foo')


def test_pynode_setParent(pymel):
    """
    Validate that our mocked pymel.PyNode.setParent method work.
    """
    parent = pymel.createNode("transform", name="parent")
    child = pymel.createNode("transform", name="child")

    child.setParent(parent)
    assert child.getParent() == parent

    child.setParent(world=True)
    assert child.getParent() is None


def test_pynode_getChildren(pymel):
    """
    Validate that out mocked pymel.PyNode.getChildren method work.
    """
    parent = pymel.createNode("transform", name="parent")
    child = pymel.createNode("transform", name="child")
    child.setParent(parent)
    assert parent.getChildren() == [child]
