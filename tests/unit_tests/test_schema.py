import pytest
from maya_mock import MockedSessionSchema
from maya_mock.base.schema import NodeTypeDef


@pytest.fixture()
def schema():
    """
    :rtype: MockedSessionSchema
    """
    return MockedSessionSchema()


def test_register_node(schema):
    """Assert when can register a node type."""
    node_def = NodeTypeDef("transform", {}, "")
    schema.register_node(node_def)
    assert schema.get_known_node_types() == ["transform"]
