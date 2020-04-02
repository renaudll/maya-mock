"""
Test cases for MockedSession
"""


def test_node_match(session):
    """Assert a node can be matched by it's name."""
    node1 = session.create_node("transform", name="A")
    assert session.get_nodes_by_match("A") == [node1]


def test_node_match_pattern(session):
    """Assert a node can be matched by a pattern with a `*`."""
    node1 = session.create_node("transform", name="transform1")
    assert session.get_nodes_by_match("transform*") == [node1]


def test_node_match_dagpath(session):
    """Assert a node can be matched by it's dagpath."""
    node1 = session.create_node("transform", name="A")
    assert session.get_nodes_by_match("|A") == [node1]


def test_ls_dag_clashes(session):
    """
    Assert that a call to `ls` will return all nodes with
    the provided name even where there's clashes.
    """
    node1 = session.create_node("transform", name="parent")
    node2 = session.create_node("transform", name="child", parent=node1)
    node3 = session.create_node("transform", name="child")

    assert session.get_nodes_by_match("child") == [node3, node2]


def test_node_match_hyerarchy(session):
    """Assert that a node in a hyerarchy match it's own name."""
    node1 = session.create_node("transform", name="A")
    node2 = session.create_node("transform", name="B", parent=node1)
    assert session.get_nodes_by_match("B") == [node2]


def test_node_match_hyerarchy_parent(session):
    """Assert that a node in a hyerarchy match a pattern with it's parent."""
    node1 = session.create_node("transform", name="A")
    node2 = session.create_node("transform", name="B", parent=node1)
    assert session.get_nodes_by_match("A|B") == [node2]


def test_node_match_hyerarchy_dagpath(session):
    """Assert that a node in a hyerarchy match it's full dagpath."""
    node1 = session.create_node("transform", name="A")
    node2 = session.create_node("transform", name="B", parent=node1)
    assert session.get_nodes_by_match("|A|B") == [node2]
