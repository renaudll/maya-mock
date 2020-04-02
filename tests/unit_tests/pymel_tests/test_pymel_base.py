"""
Test cases for MockedPymelSession
"""


def test_createNode(pymel):  # pylint: disable=invalid-name
    """Validate that the `createNode` function work as expected."""
    node = pymel.createNode("transform")
    assert isinstance(node, pymel.PyNode)
