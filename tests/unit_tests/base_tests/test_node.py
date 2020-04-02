"""
Test cases for MockedNode
"""


def test_dagpath(session):
    """Validate that the correct dagpath is returned for a node with a unique name."""
    node = session.create_node("transform")
    assert node.dagpath == "|transform1"


def test_dagpath_hierarchy(session):
    """Validate that the correct dagpath is returned for a node in a hyerarchy."""
    node1 = session.create_node("transform")
    node2 = session.create_node("transform")
    node3 = session.create_node("transform")
    node2.set_parent(node1)
    node3.set_parent(node2)

    assert node1.dagpath == "|transform1"
    assert node2.dagpath == "|transform1|transform2"
    assert node3.dagpath == "|transform1|transform2|transform3"


def test_node_melobject(session):
    """Assert that a single node will return it's name."""
    node = session.create_node("transform", name="A")
    assert node.__melobject__() == "A"


def test_node_shape_transform_melobject(session):
    """Assert creating a shape will create it's appropriate transform."""
    shape = session.create_node("mesh", name="A")
    assert shape.parent.__melobject__() == "polySurface1"


def test_node_melobject_clashing_rootnode(session):
    """
    Assert that a the mel representation of a node at root level that have
    the same name as another level will start with a `|`.
    """
    node1 = session.create_node("transform", name="A")
    node2 = session.create_node("transform", name="parent")
    session.create_node("transform", name="A", parent=node2)
    assert node1.__melobject__() == "|A"


def test_node_melobject_clashing(session):
    """Assert that a node not at root level that have the same name
    as another node will have a unique MEL representation."""
    session.create_node("transform", name="A")
    node2 = session.create_node("transform", name="parent")
    node3 = session.create_node("transform", name="A", parent=node2)
    assert node3.__melobject__() == "parent|A"
