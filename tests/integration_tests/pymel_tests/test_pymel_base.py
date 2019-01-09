# coding: utf-8
"""
Unit-tests for maya_mock pymel implementation.
"""


def test_createNode(pymel):
    """Validate that the `createNode` function work as expected."""
    node = pymel.createNode('transform')
    assert isinstance(node, pymel.PyNode)
