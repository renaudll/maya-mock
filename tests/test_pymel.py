import pytest
from maya_mock import MockedSession, MockedPymelSession


@pytest.fixture
def session():
    return MockedSession()


@pytest.fixture
def pymel(session):
    return MockedPymelSession(session)


def test_createNode(pymel):
    """
    Validate result when calling createNode without any name.
    The resulting name should have the node type as prefix and a number as suffix.
    """
    node = pymel.createNode('transform')
    assert node.name() == 'transform1'


def test_pynode_setParent(pymel):
    """
    Validate that our mocked pymel.PyNode.setParent method work.
    :return:
    """
    parent = pymel.createNode("transform", name="parent")
    child = pymel.createNode("transform", name="child")

    child.setParent(parent)
    assert child.getParent() == parent

    child.setParent(world=True)
    assert child.getParent() is None
